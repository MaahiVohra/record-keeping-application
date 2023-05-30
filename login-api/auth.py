from flask import Blueprint, request, jsonify, make_response
from werkzeug.security \
    import generate_password_hash, check_password_hash
from models import User
from __init__ import db
import jwt
from config import SECRET_KEY
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # if the request is a GET we return the login page
        return "Hello from the login page"
    else:  # if the request is POST the we check if the user exist with the password

        data = request.get_json()  # Retrieve the JSON data from the request

        # Extract the required fields from the JSON data
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = User.query.filter_by(email=email).first()
            if not user:  # wrong email
                response = {"message": "Not Found"}
                status_code = 404
            elif not check_password_hash(user.password, password):  # wrong password
                response = {"message": "Wrong Email or Password"}
                status_code = 401
            else:  # correct email or password
                payload = {'email': email}
                token = jwt.encode(
                    payload, SECRET_KEY, algorithm='HS256')
                response = {"message": "User Login Success", "token": token}
                status_code = 200
        else:
            response = {"message": "Bad Request"}
            status_code = 400
        return make_response(jsonify(response), status_code)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':  # If the request is GET we return the
        return "Hello from the signup page"
    else:
        data = request.get_json()  # Retrieve the JSON data from the request

        # Extract the required fields from the JSON data
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        if email and name and password:
            # check if the user already exists
            user = User.query.filter_by(email=email).first()
            if user:
                response = {'message': "User already exists"}
                status_code = 409
            # create a new user with the form data.
            else:
                new_user = User(email=email, name=name, password=generate_password_hash(
                    password, method='sha256'))  # add the new user to the db
                db.session.add(new_user)
                db.session.commit()
                response = {'message': "User created successfully"}
                status_code = 200
        else:
            response = {"message": "Bad Request"}
            status_code = 400
        return make_response(jsonify(response), status_code)
