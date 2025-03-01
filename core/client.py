"""Main Keycloak client implementation"""
import requests
from jose import JWTError, jwt
from typing import Dict, Optional
from .config import KeycloakSettings
from .db.manager import DatabaseManager
from .exceptions import InvalidTokenError, InsufficientPermissionsError

class KeycloakClient:
    """Handles Keycloak authentication and user management"""
    
    def __init__(self, config: KeycloakSettings):
        self.config = config
        self.db = DatabaseManager(config.db_url)
        self.jwks = self._fetch_jwks()
    
    def _fetch_jwks(self) -> Dict:
        """Fetch JSON Web Key Set from Keycloak"""
        jwks_url = f"{self.config.server_url}/realms/{self.config.realm}/protocol/openid-connect/certs"
        response = requests.get(jwks_url)
        response.raise_for_status()
        return response.json()
    
    def validate_token(self, token: str) -> Dict:
        """
        Validate JWT token against Keycloak configuration
        Returns decoded token payload
        """
        try:
            header = jwt.get_unverified_header(token)
            key = self._get_public_key(header["kid"])
            
            return jwt.decode(
                token,
                key,
                audience=self.config.client_id,
                issuer=f"{self.config.server_url}/realms/{self.config.realm}",
                options={"verify_exp": True, "leeway": self.config.token_leeway}
            )
        except JWTError as e:
            raise InvalidTokenError(str(e))
    
    def _get_public_key(self, kid: str) -> str:
        """Get public key from JWKS by key ID"""
        for key in self.jwks.get("keys", []):
            if key["kid"] == kid:
                return jwt.get_algorithm_by_name(key["alg"]).prepare_key(key)
        raise InvalidTokenError("Public key not found for given key ID")
    
    def sync_user(self, token: str):
        """Synchronize user data with local database"""
        payload = self.validate_token(token)
        user_data = {
            "id": payload["sub"],
            "username": payload.get("preferred_username"),
            "email": payload.get("email")
        }
        roles = payload.get("realm_access", {}).get("roles", [])
        self.db.sync_user(user_data, roles)