# Keycloak Auth Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready authentication library for Flask and FastAPI applications using Keycloak with SQLite database synchronization.

```python
# Example usage
from fastapi import FastAPI, Depends
from keycloak_auth.fastapi_integration import get_current_user

app = FastAPI()

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user_id": user["id"]}
```

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Database Schema](#database-schema)
6. [Error Handling](#error-handling)
7. [Security](#security-best-practices)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Features <a name="features"></a>
- ✅ Keycloak JWT authentication
- ✅ Role-based access control (RBAC)
- ✅ SQLite/PostgreSQL support
- ✅ Flask & FastAPI integration
- ✅ Automatic user synchronization
- ✅ Token validation with JWKS
- ✅ Production-ready security
- ✅ Custom exception hierarchy

## Installation <a name="installation"></a>
```bash
# Using pip
pip install keycloak-auth-library

# Development setup
git clone https://github.com/yourusername/keycloak-auth-library.git
cd keycloak-auth-library
pip install -e .
```

## Configuration <a name="configuration"></a>
Create `.env` file:
```ini
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=your-client
KEYCLOAK_CLIENT_SECRET=your-secret
DATABASE_URL=sqlite:///auth.db
```

## Usage <a name="usage"></a>

### Flask Integration
```python
from flask import Flask, g
from keycloak_auth.flask_integration import keycloak_auth

app = Flask(__name__)

@app.route("/protected")
@keycloak_auth(required_roles=["admin"])
def protected_route():
    return {"user": g.user["id"]}
```

### FastAPI Integration
```python
from fastapi import FastAPI, Depends
from keycloak_auth.fastapi_integration import get_current_user

app = FastAPI()

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user": user["id"]}
```

## Database Schema <a name="database-schema"></a>
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id TEXT REFERENCES users(id),
    role TEXT NOT NULL
);
```

## Error Handling <a name="error-handling"></a>
```python
try:
    # Authentication code
except AuthenticationError as e:
    # Handle 401 errors
except InsufficientPermissionsError:
    # Handle 403 errors
```

| Code | Error Class                 | Description                  |
|------|-----------------------------|------------------------------|
| 401  | `InvalidTokenError`         | Invalid/missing JWT          |
| 403  | `InsufficientPermissions`   | Missing required roles       |
| 500  | `ConfigurationError`        | Invalid setup                |

## Security Best Practices <a name="security-best-practices"></a>
1. Use HTTPS in production
2. Rotate secrets every 90 days
3. Enable Keycloak brute-force protection
4. Set token expiration ≤ 1 hour
5. Use database encryption
6. Regular security audits

## Deployment <a name="deployment"></a>
```yaml
# docker-compose.yml
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: change-me

  app:
    build: .
    environment:
      KEYCLOAK_SERVER_URL: http://keycloak:8080
    depends_on:
      - keycloak
```

## Troubleshooting <a name="troubleshooting"></a>
**Problem**: `ImportError: cannot import name...`  
✅ Verify package installation  
✅ Check for naming conflicts  

**Problem**: `InvalidTokenError`  
✅ Validate Keycloak configuration  
✅ Check token expiration  

**Problem**: Roles not syncing  
✅ Verify database permissions  
✅ Check Keycloak role mappings  

## License
MIT License - See [LICENSE](LICENSE) for details.