"""Custom exceptions for authentication flow"""

class AuthenticationError(Exception):
    """Base authentication exception"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message)

class InvalidTokenError(AuthenticationError):
    """JWT validation failed"""

class InsufficientPermissionsError(AuthenticationError):
    """User lacks required permissions"""

class ConfigurationError(Exception):
    """Invalid configuration provided"""