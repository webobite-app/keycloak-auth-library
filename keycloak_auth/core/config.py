"""Configuration management using Pydantic"""
from pydantic_settings import BaseSettings
from pydantic import SecretStr
class KeycloakSettings(BaseSettings):
    """
    Keycloak configuration settings with environment variables fallback
    Example .env file:
        KEYCLOAK_SERVER_URL=http://localhost:8080
        KEYCLOAK_REALM=master
        KEYCLOAK_CLIENT_ID=my-client
        KEYCLOAK_CLIENT_SECRET=secret
    """
    server_url: str
    realm: str
    client_id: str
    client_secret: SecretStr
    db_url: str = "sqlite:///auth.db"
    token_leeway: int = 30  # Seconds for clock skew allowance
    
    class Config:
        env_file = ".env"
        env_prefix = "KEYCLOAK_"