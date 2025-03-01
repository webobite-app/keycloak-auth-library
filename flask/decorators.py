"""Flask authentication decorators"""
from functools import wraps
from flask import request, g
from ..core.client import KeycloakClient
from ..core.exceptions import InvalidTokenError, InsufficientPermissionsError

def keycloak_auth(required_roles=None):
    """Decorator for Flask route authentication"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = _extract_token()
            client = _get_client()
            
            try:
                # Validate and sync user
                payload = client.validate_token(token)
                client.sync_user(token)
                
                # Check permissions
                user_roles = client.db.get_user_roles(payload["sub"])
                if required_roles and not set(required_roles).intersection(user_roles):
                    raise InsufficientPermissionsError()
                
                # Add user to request context
                g.user = {
                    "id": payload["sub"],
                    "roles": user_roles,
                    "token": token
                }
                return func(*args, **kwargs)
            
            except InvalidTokenError as e:
                return {"error": str(e)}, 401
            except InsufficientPermissionsError:
                return {"error": "Forbidden"}, 403
        
        return wrapper
    return decorator

def _extract_token() -> str:
    """Extract Bearer token from Authorization header"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise InvalidTokenError("Invalid authorization header")
    return auth_header.split(" ")[1]

def _get_client() -> KeycloakClient:
    """Get configured Keycloak client from Flask app context"""
    from flask import current_app
    return current_app.keycloak_client