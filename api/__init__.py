from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # ORM library
from config import SECRET_KEY
from flask_cors import CORS
db = SQLAlchemy()


def create_app():
    # creates the Flask instance, __name__ is the name of the current Python module
    app = Flask(__name__)
    CORS(app)
    # it is used by Flask and extensions to keep data safe
    app.config['SECRET_KEY'] = SECRET_KEY
    # the path to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialiaze sqlite database
    from router import router as router_blueprint
    app.register_blueprint(router_blueprint)
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
