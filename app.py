from flask import Flask
from keycloak_auth.flask import keycloak_auth

app = Flask(__name__)
app.keycloak_client = KeycloakClient(KeycloakSettings())

@app.route("/protected")
@keycloak_auth(required_roles=["admin"])
def protected_route():
    return {"user": g.user["id"]}


# from fastapi import FastAPI, Depends
# from keycloak_auth.fastapi import get_current_user

# app = FastAPI()

# @app.get("/protected")
# async def protected_route(user: dict = Depends(get_current_user)):
#     return {"user": user["id"]}