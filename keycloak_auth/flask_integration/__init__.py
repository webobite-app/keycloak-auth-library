# keycloak_auth/flask_integration/__init__.py
from .decorators import keycloak_auth  # Explicitly export the decorator

__all__ = ["keycloak_auth"]  # Optional but recommended