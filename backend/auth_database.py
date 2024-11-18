from sqlalchemy import select
import bcrypt

from database import UserDB, TaskDB, BlacklistTokens, db
from exceptions import CustomException

def login(username: str, password: str):
    stmt = select(UserDB).where(UserDB.username == username)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("User doesn't exist", 400)
    user: UserDB = rows[0]
    if not bcrypt.checkpw(password.encode("utf-8"), user.password):
        raise CustomException("Invalid password", 400)
    return user

def register(user: UserDB):
    stmt = select(UserDB).where(UserDB.username == user.username)
    rows = db.session.execute(stmt).one_or_none()
    if rows is not None:
        raise CustomException("Username taken", 400)
    salt = bcrypt.gensalt()
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), salt) 
    db.session.add(user)
    db.session.commit()

def logout(token: str):
    blacklist = BlacklistTokens(token)
    db.session.add(blacklist)
    db.session.commit()

def validate_token(token: str):
    stmt = select(BlacklistTokens).where(BlacklistTokens.token == token)
    rows = db.session.execute(stmt).one_or_none()
    if rows is not None:
        return False
    return True

    