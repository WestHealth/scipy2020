from __future__ import division

import base64
import datetime
import logging
import os
import sys
import uuid
import time
import yaml
from hashlib import md5
from awstools.spawner import SetupSpawner
import requests
import boto3
from jose import jwt, JOSEError

from flask import Flask, request, redirect, make_response, abort, app, jsonify, url_for, render_template
from jupyter_lib import jupyter, jupyter_dash, jupyter_status

PK_SERVER = "https://public-keys.auth.elb.us-west-2.amazonaws.com/"
region = "us-west-2"
auth_cookie_name = "DevNotebookAuthSessionCookie-0"
pk_cache=dict(key_id=None, pk=None)
with open("config.yaml") as f:
    fd_config = yaml.load(f, Loader=yaml.SafeLoader)
    url_prefix = fd_config['hub']['url_prefix']
    api_prefix = fd_config['hub']['api_url_prefix']

app = Flask(__name__, static_url_path=url_prefix.rstrip('/'))
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def authenticated(request):
    global pk_cache
    oidc_id = request.headers.get('x-amzn-oidc-identity')
    oidc_jwt = request.headers.get('x-amzn-oidc-data')
    
    if not oidc_jwt:
        app.logger.warning("No JWT Token in Header")
        return {}

    try:
        header = jwt.get_unverified_headers(oidc_jwt)
    except JOSEError as e:
        app.logger.error("JWT failed to decode: {}".format(e))
        return {}
    kid = header.get('kid')
    if not kid:
        app.logger.error("No Key ID in JWT token")
        return {};

    if not pk_cache['pk'] or pk_cache['key_id']!=kid:
        try:
            r = requests.get(PK_SERVER + kid)
            pk_cache['key_id']=kid
            pk_cache['pk'] = r.text
        except requests.RequestException as e:
            app.logger.error("Requests Error: {}".format(e))
            return {}

    try:
        token = jwt.decode(oidc_jwt, pk_cache['pk'])
    except JOSEError as e:
        app.logger.info("JWT failed to validate: {}".format(e))
        return {}


    if token['sub'] != oidc_id:
        app.logger.error("User ID in token doesn't match user ID in header")
        return {}

    return token

def get_user():
    token = authenticated(request)
    if token:
        return token['sub']

@app.route("/")
def health_check():
    return jsonify(dict(status='success'))

def dashboard():
    token = authenticated(request)
    global fd_config
    print (token)
    return jupyter_dash(authenticated(request), fd_config, fd_config['hub']['api_url_prefix'], render_template)

def api_notebook(notebook, abbr, start):
    global fd_config
    return jupyter(notebook, abbr, start, authenticated(request), fd_config, app.logger)

def api_notebook_status(notebook, abbr, start):
    global fd_config
    update=True
    if '/query' in request.path:
        update=False
    return jupyter_status(notebook, start, update, authenticated(request), fd_config, app.logger)

def login():
    return redirect(url_for("dashboard"))

def logout():
    response = make_response(redirect(url_for("dashboard")))
    response.set_cookie(auth_cookie_name, '')
    return response

def help():
    return redirect(url_for("dashboard"))


if __name__ == '__main__':
    context = ('hub.crt', 'hub.key')
    app.add_url_rule('/auth-sign-in', 'auth-sign-in', dashboard)
    app.add_url_rule(url_prefix, 'dashboard', dashboard)
    app.add_url_rule(api_prefix+'<notebook>/<abbr>/<start>/', 'api_notebook', api_notebook)
    app.add_url_rule(api_prefix+'<notebook>/<abbr>/<start>/status/', 'api_notebook_status', api_notebook_status)
    app.add_url_rule(api_prefix+'<notebook>/<abbr>/<start>/query/', 'api_notebook_status', api_notebook_status)
    app.add_url_rule(url_prefix+'login', 'login', login)
    app.add_url_rule(url_prefix+'try_again', 'try_again', login)
    app.add_url_rule(url_prefix+'logout', 'logout', logout)
    app.add_url_rule(url_prefix+'help', 'help', help)
    app.run(host="0.0.0.0", ssl_context=context, debug=True)
