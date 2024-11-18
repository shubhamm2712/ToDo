from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, Date, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

import datetime

db = SQLAlchemy()

class UserDB(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    tasks: Mapped[List["TaskDB"]] = relationship(back_populates="user")

    def __init__(self, username = None, password = None, name = None, id = None):
        if id is not None:
            self.id = id
        self.username = username
        self.password = password
        self.name = name
    
    def toJson(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name
        }

class TaskDB(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime.date] = mapped_column(Date)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    userId: Mapped[int] = mapped_column(ForeignKey("user_db.id"), nullable=False)

    user: Mapped["UserDB"] = relationship(back_populates="tasks")

    def __init__(self, description=None, date=None,status=False, userId=None, id=None):
        if id is not None:
            self.id = id
        self.description = description
        self.date = date
        self.status = status
        self.userId = userId

    def toJson(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": self.date,
            "status": self.status,
            "userId": self.userId
        }
    
class BlacklistTokens(db.Model):
    token: Mapped[str] = mapped_column(Text, primary_key=True)

    def __init__(self, token=None):
        self.token = token