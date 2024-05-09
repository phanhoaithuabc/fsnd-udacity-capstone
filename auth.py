import requests
import os
from flask import request
from functools import wraps
from jose import jwt


AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get('API_AUDIENCE')

## AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise AuthError({
                "code": "authorization_header_missing",
                "description": "Authorization header is missed"
            }, 401)
    
    header_parts = auth_header.split()
    if len(header_parts) != 2 or header_parts[0].lower() != "bearer":
        raise AuthError({
                "code": "invalid_header",
                "description": "Authorization header doesn't start with Bearer"
            }, 401)
    print(header_parts[1])
    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
                'code': 'invalid_permissions',
                'description': 'User doesn\'t have roles attached'
            }, 401)

    token_scopes = payload['permissions']
    if permission not in token_scopes:
        raise AuthError({
                'code': 'invalid_permissions',
                'description': 'User doesn\'t have enough privileges'
            }, 401)
    
    return True


def get_jwks():
    response = requests.get(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    response.raise_for_status()
    return response.json()

def get_rsa_key(jwks, kid):
    for key in jwks['keys']:
        if key['kid'] == kid:
            return {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    return None

def verify_decode_jwt(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
                'code': 'invalid_header', 
                'description': 'Authorization malformed.'
            }, 401)

    rsa_key = get_rsa_key(jwks, unverified_header['kid'])

    if rsa_key:
        try:
            payload = jwt.decode(token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/')
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                    'code': 'token_expired', 
                    'description': 'Token expired'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                    'code': 'invalid_claims', 
                    'description': 'Incorrect claims'
                }, 401)
        
        except jwt.InvalidTokenError:
            raise AuthError({
                    'code': 'invalid_token', 
                    'description': 'Invalid token'
                }, 401)
        
        except Exception:
            raise AuthError({
                    'code': 'invalid_header', 
                    'description': 'Unable to parse token.'
                }, 400)
    raise AuthError({
            'code': 'invalid_header', 
            'description': 'Unable to find the header'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator