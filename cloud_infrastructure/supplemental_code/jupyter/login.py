"""Tornado handlers for logging into the notebook."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import re

import requests
import tornado
from jose import jwt, JOSEError

try:
    from urllib.parse import urlparse # Py 3
except ImportError:
    from urlparse import urlparse # Py 2
import uuid

from tornado.escape import url_escape

from .security import passwd_check, set_password

from ..base.handlers import IPythonHandler

user_cache = dict(container_uid=None)
PK_SERVER = "https://public-keys.auth.elb.us-west-2.amazonaws.com/"
ID_FILE = '/usr/local/gateway/id'

class LoginHandler(IPythonHandler):
    """The basic tornado login handler

    authenticates with a hashed password from the configuration.
    """
    def _render(self, message=None):
        self.write(self.render_template('login.html',
                next=url_escape(self.get_argument('next', default=self.base_url)),
                message=message,
        ))

    def _redirect_safe(self, url, default=None):
        """Redirect if url is on our PATH

        Full-domain redirects are allowed if they pass our CORS origin checks.

        Otherwise use default (self.base_url if unspecified).
        """
        if default is None:
            default = self.base_url
        if not url.startswith(self.base_url):
            # require that next_url be absolute path within our path
            allow = False
            # OR pass our cross-origin check
            if '://' in url:
                # if full URL, run our cross-origin check:
                parsed = urlparse(url.lower())
                origin = '%s://%s' % (parsed.scheme, parsed.netloc)
                if self.allow_origin:
                    allow = self.allow_origin == origin
                elif self.allow_origin_pat:
                    allow = bool(self.allow_origin_pat.match(origin))
            if not allow:
                # not allowed, use default
                self.log.warning("Not allowing login redirect to %r" % url)
                url = default
        self.redirect(url)

    @tornado.gen.coroutine
    def get(self):
        authenticated = False
        if self.current_user:
            authenticated = True
        else:
            if self.verify_jwt():
                authenticated=True

        self.log.debug("VERIFY: {}".format(authenticated))
        
        if authenticated:
            next_url = self.get_argument('next', default=self.base_url)
            self._redirect_safe(next_url)
        else:
            self._render()

    def verify_jwt(self):
        global user_cache
        oidc_id = self.request.headers.get('x-amzn-oidc-identity')
        oidc_jwt = self.request.headers.get('x-amzn-oidc-data')
        self.log.debug("Getting ID: {}".format(oidc_id))
        
        if not oidc_jwt:
            self.log.warning("No JWT Token in Header")
            return False

        if os.path.exists(ID_FILE):
            with open(ID_FILE, "r") as f:
                user_cache['container_uid'] = f.read()
                
        if not user_cache['container_uid'] is None:
            if oidc_id != user_cache['container_uid']:
                self.log.error(
                    "Mismatch between header ID and container User ID: {} - {}".format(oidc_id, user_cache['container_uid']))
                return False

        if (user_cache.get('user_id') == oidc_id and oidc_id == user_cache['container_uid'] and user_cache.get(
                'jwt') == oidc_jwt):
            return True

        try:
            header = jwt.get_unverified_headers(oidc_jwt)
        except JOSEError as e:
            self.log.error("JWT failed to decode: {}".format(e))
            return False

        kid = header.get('kid')
        if not kid:
            self.log.error("No Key ID in JWT token")
            return False

        if kid != user_cache.get('kid'):
            if 'pk' in user_cache:
                del user_cache['pk']

        if not 'pk' in user_cache:
            try:
                r = requests.get(PK_SERVER + kid)
                # TODO treat return code
                user_cache['pk'] = r.text
                user_cache['kid'] = kid
            except requests.RequestException as e:
                self.log.error("Requests Error: {}".format(e))
                return False

        try:
            token = jwt.decode(oidc_jwt, user_cache['pk'])
        except JOSEError as e:
            self.log.info("JWT failed to validate: {}".format(e))
            return False

        if token['sub'] != oidc_id:
            self.log.error("User ID in token doesn't match user ID in header")
            return False

        user_cache['user_id'] = oidc_id
        user_cache['jwt'] = oidc_jwt

        if user_cache['container_uid'] is None:
            with open(ID_FILE, 'x') as f:
                f.write(oidc_id)
                user_cache['container_uid'] = oidc_id
        return True

    
    @property
    def hashed_password(self):
        return self.password_from_settings(self.settings)

    def passwd_check(self, a, b):
        return passwd_check(a, b)
    
    def post(self):
        typed_password = self.get_argument('password', default=u'')
        new_password = self.get_argument('new_password', default=u'')


        
        if self.get_login_available(self.settings):
            if self.passwd_check(self.hashed_password, typed_password) and not new_password:
                self.set_login_cookie(self, uuid.uuid4().hex)
            elif self.token and self.token == typed_password:
                self.set_login_cookie(self, uuid.uuid4().hex)
                if new_password and self.settings.get('allow_password_change'):
                    config_dir = self.settings.get('config_dir')
                    config_file = os.path.join(config_dir, 'jupyter_notebook_config.json')
                    set_password(new_password, config_file=config_file)
                    self.log.info("Wrote hashed password to %s" % config_file)
            else:
                self.set_status(401)
                self._render(message={'error': 'Invalid credentials'})
                return


        next_url = self.get_argument('next', default=self.base_url)
        self._redirect_safe(next_url)

    @classmethod
    def set_login_cookie(cls, handler, user_id=None):
        """Call this on handlers to set the login cookie for success"""
        cookie_options = handler.settings.get('cookie_options', {})
        cookie_options.setdefault('httponly', True)
        # tornado <4.2 has a bug that considers secure==True as soon as
        # 'secure' kwarg is passed to set_secure_cookie
        if handler.settings.get('secure_cookie', handler.request.protocol == 'https'):
            cookie_options.setdefault('secure', True)
        cookie_options.setdefault('path', handler.base_url)
        handler.set_secure_cookie(handler.cookie_name, user_id, **cookie_options)
        return user_id

    auth_header_pat = re.compile('token\s+(.+)', re.IGNORECASE)

    @classmethod
    def get_token(cls, handler):
        """Get the user token from a request

        Default:

        - in URL parameters: ?token=<token>
        - in header: Authorization: token <token>
        """

        user_token = handler.get_argument('token', '')
        if not user_token:
            # get it from Authorization header
            m = cls.auth_header_pat.match(handler.request.headers.get('Authorization', ''))
            if m:
                user_token = m.group(1)
        return user_token

    @classmethod
    def should_check_origin(cls, handler):
        """Should the Handler check for CORS origin validation?

        Origin check should be skipped for token-authenticated requests.

        Returns:
        - True, if Handler must check for valid CORS origin.
        - False, if Handler should skip origin check since requests are token-authenticated.
        """
        return not cls.is_token_authenticated(handler)

    @classmethod
    def is_token_authenticated(cls, handler):
        """Returns True if handler has been token authenticated. Otherwise, False.

        Login with a token is used to signal certain things, such as:

        - permit access to REST API
        - xsrf protection
        - skip origin-checks for scripts
        """
        if getattr(handler, '_user_id', None) is None:
            # ensure get_user has been called, so we know if we're token-authenticated
            handler.get_current_user()
        return getattr(handler, '_token_authenticated', False)

    @classmethod
    def get_user(cls, handler):
        """Called by handlers.get_current_user for identifying the current user.

        See tornado.web.RequestHandler.get_current_user for details.
        """
        # Can't call this get_current_user because it will collide when
        # called on LoginHandler itself.
        if getattr(handler, '_user_id', None):
            return handler._user_id
        user_id = cls.get_user_token(handler)
        if user_id is None:
            get_secure_cookie_kwargs  = handler.settings.get('get_secure_cookie_kwargs', {})
            user_id = handler.get_secure_cookie(handler.cookie_name, **get_secure_cookie_kwargs )
        else:
            cls.set_login_cookie(handler, user_id)
            # Record that the current request has been authenticated with a token.
            # Used in is_token_authenticated above.
            handler._token_authenticated = True
        if user_id is None:
            # If an invalid cookie was sent, clear it to prevent unnecessary
            # extra warnings. But don't do this on a request with *no* cookie,
            # because that can erroneously log you out (see gh-3365)
            if handler.get_cookie(handler.cookie_name) is not None:
                handler.log.warning("Clearing invalid/expired login cookie %s", handler.cookie_name)
                handler.clear_login_cookie()
            if not handler.login_available:
                # Completely insecure! No authentication at all.
                # No need to warn here, though; validate_security will have already done that.
                user_id = 'anonymous'

        # cache value for future retrievals on the same request
        handler._user_id = user_id
        return user_id

    @classmethod
    def get_user_token(cls, handler):
        """Identify the user based on a token in the URL or Authorization header
        
        Returns:
        - uuid if authenticated
        - None if not
        """

        authenticated = False
        if cls.verify_oidc(handler):
            authenticated = True
        else:
            oidc_jwt = handler.request.headers.get('x-amzn-oidc-data')
            if oidc_jwt:
                try:
                    header = jwt.get_unverified_headers(oidc_jwt)
                except JOSEError:
                    return None
                kid = header.get('kid')
                if kid and kid == user_cache.get('kid') and user_cache.get('pk'):
                    try:
                        token = jwt.decode(oidc_jwt, user_cache['pk'])
                    except JOSEError:
                        return None
                    oidc_id = handler.request.headers.get('x-amzn-oidc-identity')
                    if token['sub'] == oidc_id and oidc_id == user_cache.get('container_uid'):
                        authenticated = True
                        user_cache['jwt'] = oidc_jwt
                        user_cache['user_id'] = oidc_id
                        

        handler.log.info("Authenicated = {}".format (authenticated))
        if authenticated:
            return uuid.uuid4().hex
        else:
            return None

    @classmethod
    def verify_oidc(cls, handler):
        global user_cache
        oidc_id = handler.request.headers.get('x-amzn-oidc-identity')
        oidc_jwt = handler.request.headers.get('x-amzn-oidc-data')
        oidc_access = handler.request.headers.get('x-amzn-oidc-accesstoken')

        handler.log.debug("IDs: {}, {}, {}".format(oidc_id, oidc_access, oidc_jwt))
                     
        if oidc_id != user_cache.get('container_uid'):
            return False
            
        if not oidc_id or not oidc_jwt:
            return False
        if oidc_id != user_cache.get('user_id'):
            return False
        if oidc_jwt != user_cache.get('jwt'):
            return False
        try:
            header = jwt.get_unverified_headers(oidc_jwt)
        except JOSEError:
            return False
        kid = header.get('kid')
        if kid != user_cache.get('kid'):
            return False

        # TODO: TIMESTAMP CHECK
        return True

        


    @classmethod
    def validate_security(cls, app, ssl_options=None):
        """Check the notebook application's security.

        Show messages, or abort if necessary, based on the security configuration.
        """
        if not app.ip:
            warning = "WARNING: The notebook server is listening on all IP addresses"
            if ssl_options is None:
                app.log.warning(warning + " and not using encryption. This "
                    "is not recommended.")
            if not app.password and not app.token:
                app.log.warning(warning + " and not using authentication. "
                    "This is highly insecure and not recommended.")
        else:
            if not app.password and not app.token:
                app.log.warning(
                    "All authentication is disabled."
                    "  Anyone who can connect to this server will be able to run code.")

    @classmethod
    def password_from_settings(cls, settings):
        """Return the hashed password from the tornado settings.

        If there is no configured password, an empty string will be returned.
        """
        return settings.get('password', u'')

    @classmethod
    def get_login_available(cls, settings):
        """Whether this LoginHandler is needed - and therefore whether the login page should be displayed."""
        return bool(cls.password_from_settings(settings) or settings.get('token'))
