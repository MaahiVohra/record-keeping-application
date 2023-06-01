from flask import Blueprint, jsonify, make_response
from __init__ import create_app, db
main = Blueprint('main', __name__)


@main.route('/')  # home page for the api server
def index():
    return "Hello from the api"


app = create_app()
if __name__ == '__main__':  # ensures it only runs when the script is executed not when used as a module
    with app.app_context():  # establishes application context
        db.create_all()  # creates tables inside the database according to the models
    app.run(debug=True)
