from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..core.client import KeycloakClient
from ..core.config import KeycloakSettings
from ..core.exceptions import InvalidTokenError, InsufficientPermissionsError

security = HTTPBearer()

# Define helper functions first
def get_settings() -> KeycloakSettings:
    """Dependency for configuration settings"""
    return KeycloakSettings()

def get_keycloak_client(settings: KeycloakSettings = Depends(get_settings)) -> KeycloakClient:
    """Dependency for Keycloak client"""
    return KeycloakClient(settings)

# Then define the main dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    client: KeycloakClient = Depends(get_keycloak_client)
) -> dict:
    try:
        token = credentials.credentials
        payload = client.validate_token(token)
        client.sync_user(token)
        return {
            "id": payload["sub"],
            "roles": client.db.get_user_roles(payload["sub"]),
            "token": token
        }
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )