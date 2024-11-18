from datetime import datetime
from flask import Blueprint, request

import auth_business
import tasks_database
from database import TaskDB
from exceptions import CustomException

bp = Blueprint("task_blueprint", __name__, url_prefix="/task")

@bp.route("/", methods=["GET", "POST"])
def get_tasks():
    try:
        user, token = auth_business.verify_token()
        if request.method == "GET":
            return tasks_database.get_tasks(user)
        else:
            data = request.get_json()
            description = data.get("description", "").strip()
            description = description or None
            date: datetime.date = data.get("date", datetime.today())
            if description is None or date is None:
                raise CustomException("Missing data", 400)
            task = TaskDB(description, date, False, user.id)
            tasks_database.add_task(user, task)
            return {"message": "successfully added"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500

@bp.route("/complete", methods=["PUT"])
def complete():
    try:
        user, token = auth_business.verify_token()
        data = request.get_json()
        taskId = data.get("taskId", None)
        if taskId is None:
            raise CustomException("Missing", 400)
        status = data.get("status", False)
        if type(taskId) == str:
            if taskId.isnumeric():
                taskId = int(taskId)
            else:
                raise CustomException("Invalid", 400)
        if type(taskId) != int:
            raise CustomException("Invalid", 400)
        tasks_database.complete_task(user, taskId, status)
        return {"message": "successfully updated"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500

@bp.route("/update", methods=["PUT"])
def update():
    try:
        user, token = auth_business.verify_token()
        data = request.get_json()
        taskId = data.get("taskId", None)
        if taskId is None:
            raise CustomException("Missing", 400)
        description = data.get("description", "").strip()
        if not description:
            raise CustomException("Missing data", 400)
        if type(taskId) == str:
            if taskId.isnumeric():
                taskId = int(taskId)
            else:
                raise CustomException("Invalid", 400)
        if type(taskId) != int:
            raise CustomException("Invalid", 400)
        tasks_database.update_task(user, taskId, description)
        return {"message": "successfully updated"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500

@bp.route("/<taskId>", methods=["DELETE"])
def delete_tasks(taskId: int):
    try:
        user, token = auth_business.verify_token()
        tasks_database.delete_task(user, taskId)
        return {"message": "Successfully deleted"}
    except CustomException as e:
        return e.toResponse()
    except Exception as e:
        return {"message": "Exception: "+str(e)}, 500