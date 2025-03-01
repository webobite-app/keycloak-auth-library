"""FastAPI dependency injection setup"""
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..core.client import KeycloakClient
from ..core.config import KeycloakSettings
from ..core.exceptions import InvalidTokenError, InsufficientPermissionsError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    client: KeycloakClient = Depends(get_keycloak_client)
) -> dict:
    """FastAPI dependency for authenticated users"""
    try:
        token = credentials.credentials
        payload = client.validate_token(token)
        client.sync_user(token)
        
        # Get roles from database
        user_roles = client.db.get_user_roles(payload["sub"])
        
        return {
            "id": payload["sub"],
            "roles": user_roles,
            "token": token
        }
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InsufficientPermissionsError:
        raise HTTPException(status_code=403, detail="Forbidden")

def get_keycloak_client(settings: KeycloakSettings = Depends(get_settings)) -> KeycloakClient:
    """Dependency for Keycloak client"""
    return KeycloakClient(settings)

def get_settings() -> KeycloakSettings:
    """Dependency for configuration settings"""
    return KeycloakSettings()