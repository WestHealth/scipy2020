from websockify.websockifyserver import WebSockifyServer
from jose import jwt, JOSEError
import requests
import sys, os
class BasePlugin(object):
    def __init__(self, src=None):
        self.source = src

    def authenticate(self, headers, target_host, target_port):
        pass


class AuthenticationError(Exception):
    def __init__(self, log_msg=None, response_code=403, response_headers={}, response_msg=None):
        self.code = response_code
        self.headers = response_headers
        self.msg = response_msg

        if log_msg is None:
            log_msg = response_msg

        super(AuthenticationError, self).__init__('%s %s' % (self.code, log_msg))


class InvalidOriginError(AuthenticationError):
    def __init__(self, expected, actual):
        self.expected_origin = expected
        self.actual_origin = actual

        super(InvalidOriginError, self).__init__(
            response_msg='Invalid Origin',
            log_msg="Invalid Origin Header: Expected one of "
                    "%s, got '%s'" % (expected, actual))


class BasicHTTPAuth(object):
    """Verifies Basic Auth headers. Specify src as username:password"""

    def __init__(self, src=None):
        self.src = src

    def authenticate(self, headers, target_host, target_port):
        import base64
        auth_header = headers.get('Authorization')
        if auth_header:
            if not auth_header.startswith('Basic '):
                self.auth_error()

            try:
                user_pass_raw = base64.b64decode(auth_header[6:])
            except TypeError:
                self.auth_error()

            try:
                # http://stackoverflow.com/questions/7242316/what-encoding-should-i-use-for-http-basic-authentication
                user_pass_as_text = user_pass_raw.decode('ISO-8859-1')
            except UnicodeDecodeError:
                self.auth_error()

            user_pass = user_pass_as_text.split(':', 1)
            if len(user_pass) != 2:
                self.auth_error()

            if not self.validate_creds(*user_pass):
                self.demand_auth()

        else:
            self.demand_auth()

    def validate_creds(self, username, password):
        if '%s:%s' % (username, password) == self.src:
            return True
        else:
            return False

    def auth_error(self):
        raise AuthenticationError(response_code=403)

    def demand_auth(self):
        raise AuthenticationError(response_code=401,
                                  response_headers={'WWW-Authenticate': 'Basic realm="Websockify"'})

class ExpectOrigin(object):
    def __init__(self, src=None):
        if src is None:
            self.source = ['https://localhost:6901']
        else:
            self.source = src.split()

    def authenticate(self, headers, target_host, target_port):
        origin = headers.get('Origin', None)
        if origin is None or origin not in self.source:
            raise InvalidOriginError(expected=self.source, actual=origin)

class ClientCertCNAuth(object):
    """Verifies client by SSL certificate. Specify src as whitespace separated list of common names."""

    def __init__(self, src=None):
        if src is None:
            self.source = []
        else:
            self.source = src.split()

    def authenticate(self, headers, target_host, target_port):
        if headers.get('SSL_CLIENT_S_DN_CN', None) not in self.source:
            raise AuthenticationError(response_code=403)

PK_SERVER = "https://public-keys.auth.elb.us-west-2.amazonaws.com/"
region = "us-west-2"
pk_cache=dict(key_id=None, pk=None)


class AmazonAuth(object):
    def __init__(self, src=None):
        self.src = src
        WebSockifyServer = sys.modules['websockify.websockifyserver'].WebSockifyServer
        self.logger=WebSockifyServer.get_logger()
        
    def authenticate(self, headers, target_host, target_port):
        global pk_cache
        oidc_id = headers.get('X-Amzn-Oidc-Identity')
        oidc_jwt = headers.get('X-Amzn-Oidc-Data')

        if not oidc_jwt:
            self.logger.warning("No JWT Token in Header")
            self.auth_error()
        if oidc_id != os.environ.get("OIDC_ID"):
            self.logger.warning("User ID Mismatch")
            self.auth_error()
        
        try:
            header = jwt.get_unverified_headers(oidc_jwt)
        except JOSEError as e:
            self.logger.error("JWT failed to decode: {}".format(e))
            self.auth_error()
            
        kid = header.get('kid')
        if not kid:
            self.logger.error("No Key ID in JWT token")
            self.auth_error()

        if not pk_cache['pk'] or pk_cache['key_id']!=kid:
            try:
                r = requests.get(PK_SERVER + kid)
                pk_cache['key_id']=kid
                pk_cache['pk'] = r.text
            except requests.RequestException as e:
                self.logger.error("Requests Error: {}".format(e))
                self.auth_error()

        try:
            token = jwt.decode(oidc_jwt, pk_cache['pk'])
        except JOSEError as e:
            self.logger.info("JWT failed to validate: {}".format(e))
            self.auth_error()


        if token['sub'] != oidc_id:
            self.logger.error("User ID in token doesn't match user ID in header")
            self.auth_error()
        self.logger.info("User {} authenticated".format(oidc_id))

    def auth_error(self):
        raise AuthenticationError(response_code=403)

