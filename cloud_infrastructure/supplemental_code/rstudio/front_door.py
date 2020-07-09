from __future__ import division

import base64
import datetime
import logging
import os
import sys
import uuid
from config import USER
import requests
from jose import jwt, JOSEError

if sys.version_info[0] < 3:
    from urllib import quote
else:
    from urllib.parse import quote

from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from flask import Flask, request, redirect, make_response, abort, app, jsonify
import time

PK_SERVER = "https://public-keys.auth.elb.us-west-2.amazonaws.com/"
ID_FILE = '/usr/local/gateway/id'
app = Flask(__name__)
RS_KEY_FILE='/var/lib/rstudio-server/secure-cookie-key'
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


while not os.path.exists(RS_KEY_FILE):
    time.sleep(1)
    
with open(RS_KEY_FILE) as f:
    secret = f.read()

container_uid = None

if os.path.isfile(ID_FILE):
    with open(ID_FILE) as f:
        container_uid = f.read()


@app.route("/rstudio/"+USER+"/auth-sign-out", methods=['GET', "POST"])
@app.route("/auth-sign-out", methods=['GET', "POST"])
def sign_out():
    return redirect(os.environ['logout_url'])

@app.route("/ping")
def health_check():
    return jsonify(dict(status='success'))

@app.route("/rstudio/"+USER+"/auth-sign-in", methods=['GET', "POST"])
@app.route("/auth-sign-in", methods=['GET', "POST"])
def sign_in():
    global container_uid
    oidc_id = request.headers.get('x-amzn-oidc-identity')
    oidc_jwt = request.headers.get('x-amzn-oidc-data')
    if sys.version_info[0] < 3:
        create = "wx"
    else:
        create = "x"

    def rstudio_cookie(username, secret, validity_days=30):
        """ Generates an RStudio Server `user-id` cookie string.
        
        This cookie string is of the form: `user_id|expiry|hmac`
        Where the HMAC is calculated as `HMAC_SHA256(user_id+expiry, secret)`
        
        All input strings should be in un-escaped format.
        The output string will be properly URL-escaped.
        
        :param str username: Full username
        :param str secret: Server secret cookie value
        This value is typically found in `/var/lib/rstudio-server/secure-cookie-key`
        and is an arbitrary string (but is typically a random hex encoded value)
        :param str validity_days: Number of days to set the validity for this login token.
        The default is 30 days (same as RStudio Server).  However, this could be
        set to a value that matches the SAML or JWT token validity.
        
        :return: URL encoded string that can be directly set as the `user-id` cookie value.
        This value is already properly URL escaped in a format that RStudio Server
        will accept.
        :rtype: str
        """

        utc = datetime.datetime.utcnow()
        val = utc + datetime.timedelta(validity_days)
        now = val.strftime('%a, %d %b %Y %H:%M:%S GMT')
        dig = base64.b64encode(HMAC.new(secret, "{0}{1}".format(username, now), digestmod=SHA256).digest())
        app.logger.debug("Parts: {}, {}, {}, {}".format(secret, username, now, type(dig)))
        return quote("{0}|{1}|{2}".format(username, now, dig.decode()), '|')

    if not oidc_jwt:
        app.logger.warning("No JWT Token in Header")
        abort(401)

    if not container_uid is None:
        if oidc_id != container_uid:
            app.logger.error("Mismatch between header ID and container User ID: {} - {}".format(oidc_id, container_uid))
            abort(401)

    try:
        header = jwt.get_unverified_headers(oidc_jwt)
    except JOSEError as e:
        app.logger.error("JWT failed to decode: {}".format(e))
        abort(401)
    kid = header.get('kid')
    if not kid:
        app.logger.error("No Key ID in JWT token")
        abort(401);
    try:
        r = requests.get(PK_SERVER + kid)
        token = jwt.decode(oidc_jwt, r.text)
    except JOSEError as e:
        app.logger.info("JWT failed to validate: {}".format(e))
        abort(401)

    except requests.RequestException as e:
        app.logger.error("Requests Error: {}".format(e))
        abort(401)

    if token['sub'] != oidc_id:
        app.logger.error("User ID in token doesn't match user ID in header")
        abort(401)

    if container_uid is None:
        with open(ID_FILE, create) as f:
            f.write(oidc_id)
            container_uid = oidc_id

    response = make_response(redirect('/rstudio/'+USER+'/'))
    username = 'rstudio'
    cookie = rstudio_cookie(username, secret)
    app.logger.debug("Setting Cookie: {}".format(cookie))
    response.set_cookie('user-id', cookie)
    response.set_cookie('csrf-token', str(uuid.uuid4()), domain='.whilabs.org')
    return response


if __name__ == '__main__':
    context = ('rstudio_server.crt', 'rstudio_server.key')
    app.run(host="0.0.0.0")
