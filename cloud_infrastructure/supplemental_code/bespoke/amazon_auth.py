from jose import jwt, JOSEError
import requests

PK_SERVER = "https://public-keys.auth.elb.us-west-2.amazonaws.com/"
region = "us-west-2"
pk_cache=dict(key_id=None, pk=None)

def authenticated(app, request):
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

def login_required(func):
    '''
    taken from flask_login
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            user = authenticated(current_app, request)
            if user:
                return redirect(url_for('root.login'))
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
