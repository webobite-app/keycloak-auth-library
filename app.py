# from flask import Flask
# from keycloak_auth.flask_integration import keycloak_auth

# app = Flask(__name__)

# @app.route("/protected")
# @keycloak_auth(required_roles=["admin"])
# def protected_route():
#     return {"message": "Authenticated successfully"}
# if __name__ == "__main__":
#     app.run()

from fastapi import FastAPI, Depends
from keycloak_auth.fastapi_integration import get_current_user

app = FastAPI()

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user": user["id"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)



