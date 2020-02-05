from flask import Blueprint

db_api = Blueprint('db_api', __name__)

@db_api.route("/db")
def accountList():
    return "db data"