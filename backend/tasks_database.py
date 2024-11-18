from sqlalchemy import select

from database import UserDB, TaskDB, db
from exceptions import CustomException

def get_tasks(user: UserDB):
    stmt = select(UserDB).where(UserDB.id == user.id)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("Invalid user", 400)
    user: UserDB = rows[0]
    tasks = [task.toJson() for task in user.tasks]
    return tasks

def add_task(user: UserDB, task: TaskDB):
    stmt = select(UserDB).where(UserDB.id == user.id)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("Invalid user", 400)
    user = rows[0]
    task.user = user
    db.session.add(task)
    db.session.commit()

def complete_task(user: UserDB, taskId: int, status: bool):
    stmt = select(TaskDB).where(TaskDB.id == taskId)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("Task not present", 400)
    task: TaskDB = rows[0]
    if task.userId != user.id:
        raise CustomException("Task not yours", 400)
    task.status = status
    db.session.commit()

def update_task(user: UserDB, taskId: int, description: str):
    stmt = select(TaskDB).where(TaskDB.id == taskId)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("Task not present", 400)
    task: TaskDB = rows[0]
    if task.userId != user.id:
        raise CustomException("Task not yours", 400)
    task.description = description
    db.session.commit()

def delete_task(user: UserDB, taskId: int):
    stmt = select(TaskDB).where(TaskDB.id == taskId)
    rows = db.session.execute(stmt).one_or_none()
    if rows is None:
        raise CustomException("Task not present", 400)
    task: TaskDB = rows[0]
    if task.userId != user.id:
        raise CustomException("Task not yours", 400)
    db.session.delete(task)
    db.session.commit()
