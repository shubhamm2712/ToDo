from flask import Flask

import auth_blueprint
import tasks_blueprint
from config import config
from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_blueprint.bp)
app.register_blueprint(tasks_blueprint.bp)

@app.route("/")
def home():
    return {"message": "home"}