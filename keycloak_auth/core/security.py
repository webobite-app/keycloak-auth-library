"""
Production-grade secret management with multiple backends
"""
from typing import Optional
from pydantic import BaseSettings, SecretStr
import hvac
import boto3
import os

class SecretManager:
    def __init__(self, use_vault: bool = False):
        self.backends = [
            self._get_env_secret,
            self._get_vault_secret if use_vault else None,
            self._get_aws_secret,
        ]

    def get_secret(self, key: str) -> Optional[SecretStr]:
        """Get secret from prioritized sources"""
        for backend in filter(None, self.backends):
            secret = backend(key)
            if secret:
                return secret
        return None

    def _get_env_secret(self, key: str) -> Optional[SecretStr]:
        return os.getenv(key)

    def _get_vault_secret(self, key: str) -> Optional[SecretStr]:
        if not os.getenv("VAULT_ADDR"):
            return None
            
        client = hvac.Client(
            url=os.getenv("VAULT_ADDR"),
            token=os.getenv("VAULT_TOKEN")
        )
        secret_path = os.getenv("VAULT_SECRET_PATH", "secret/data/keycloak")
        
        return client.read(secret_path)["data"]["data"].get(key)

    def _get_aws_secret(self, key: str) -> Optional[SecretStr]:
        if not os.getenv("AWS_SECRET_NAME"):
            return None
            
        client = boto3.client("secretsmanager")
        return client.get_secret_value(
            SecretId=os.getenv("AWS_SECRET_NAME")
        ).get(key)