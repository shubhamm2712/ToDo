from flask import Blueprint, request

import auth_business
import auth_database
from database import UserDB
from exceptions import CustomException

bp = Blueprint("auth_blueprint", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        username = username or None
        password = data.get("password", "").strip()
        password = password or None
        if username is None or password is None:
            raise CustomException("Username or Password is missing", 400)
        token = auth_business.login(username, password)
        return {"access_token": token}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        name = data.get("name", "").strip()
        username = username or None
        password = password or None
        name = name or None
        if username is None or password is None or name is None:
            raise CustomException("Missing something", 400)
        user = UserDB(username, password, name)
        auth_database.register(user)
        return {"message": "Successfully registered"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500

@bp.route("/logout")
def logout():
    try:
        user, token = auth_business.verify_token()
        auth_database.logout(token)
        return {"message": "Successfully logged out"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500
    