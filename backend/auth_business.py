from datetime import datetime, timedelta
from flask import request
import jwt

import auth_database
from config import config
from database import UserDB
from exceptions import CustomException

def login(username: str, password: str):
    try:
        user: UserDB = auth_database.login(username, password)
        exp = datetime.now() + timedelta(minutes=30)
        payload = {
            "user": user.toJson(),
            "exp": exp.timestamp()
        }
        token = jwt.encode(payload, config.secret_key, algorithm="HS256")
        return token
    except CustomException as e:
        raise e
    except Exception as e:
        raise CustomException("Exception: "+str(e), 500)

def verify_token():
    try:
        if "Authorization" not in request.headers:
            raise CustomException("Authorization missing", 401)
        bearer_token = request.headers["Authorization"]
        if not bearer_token.startswith("Bearer "):
            raise CustomException("Invalid bearer token", 401)
        token = bearer_token.split(" ")[1]
        payload = jwt.decode(token, config.secret_key, algorithms="HS256")
        if "user" not in payload:
            raise CustomException("Invalid token", 401)
        if not auth_database.validate_token(token):
            raise CustomException("You have logged out", 401)
        user = UserDB(**payload["user"])
        return user, token
    except CustomException as e:
        raise e
    except jwt.exceptions.ExpiredSignatureError as e:
        raise CustomException("Token Expired", 401)
    except Exception as e:
        raise CustomException("Exception: "+str(e), 500)
