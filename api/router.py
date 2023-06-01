from flask import Blueprint, request, jsonify, make_response
from werkzeug.security \
    import generate_password_hash, check_password_hash
from models import User, Sample
from __init__ import db
from sqlalchemy import func
import jwt
import requests
import random
from config import SECRET_KEY
from functools import wraps
router = Blueprint('router', __name__)

# Decorator to create a protected route


def protected_route(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "routerorization" in request.headers:
            token = request.headers["routerorization"].split(" ")[1]
        if not token:
            return {
                "message": "routerentication Token is missing!",
                "data": None,
                "error": "Unrouterorized"
            }, 401
        try:
            data = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(email=data["email"]).first()
            if not current_user:
                return {
                    "message": "Invalid routerentication token!",
                    "data": None,
                    "error": "Unrouterorized"
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "current_user": current_user.email
            }, 500

        return f(*args, **kwargs)

    return decorated


@router.route('/login', methods=['GET', 'POST'])
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

                response = {"message": "User Login Success",
                            "token": token, "user": {
                                "id": user.id,
                                "name": user.name,
                                "email": user.email
                            }}
                status_code = 200
        else:
            response = {"message": "Bad Request"}
            status_code = 400
        return make_response(jsonify(response), status_code)


@router.route('/register', methods=['GET', 'POST'])
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


@router.route('/getRecords', methods=['GET'])
@protected_route
def get_records():
    # Protected route code

    # Retrieve records from the database and process the data
    total_records = Sample.query.count()
    # Retrieve the count of distinct values for each variable
    gender_count = db.session.query(Sample.gender, func.count(
        Sample.gender)).group_by(Sample.gender).all()
    nationality_count = db.session.query(Sample.nationality, func.count(
        Sample.nationality)).group_by(Sample.nationality).all()
    employment_type_count = db.session.query(Sample.employment_type, func.count(
        Sample.employment_type)).group_by(Sample.employment_type).all()
    age_count = db.session.query(Sample.age, func.count(
        Sample.age)).group_by(Sample.age).all()

    # Format the results as dictionaries
    gender_counts = {row[0]: row[1] for row in gender_count}
    nationality_counts = {row[0]: row[1] for row in nationality_count}
    employment_type_counts = {row[0]: row[1] for row in employment_type_count}
    age_counts = {row[0]: row[1] for row in age_count}
    age_categories = {
        "<18": 0,
        "18-40": 0,
        "40-60": 0,
        ">60": 0
    }

    for age, count in age_counts.items():
        age = int(age)  # Convert age from string to integer
        if age < 18:
            age_categories["<18"] += count
        elif 18 <= age < 40:
            age_categories["18-40"] += count
        elif 40 <= age < 60:
            age_categories["40-60"] += count
        else:
            age_categories[">60"] += count
    # Return the counts to the frontend
    response = {
        "total_records": total_records,
        "data": {
            "Gender": gender_counts,
            "Nationality": nationality_counts,
            "Employment Type": employment_type_counts,
            "Age": age_categories
        }
    }
    return make_response(jsonify(response), 200)
    # Return the processed data to the frontend in JSON format


employment_type = ["Full-time", "Part-time",
                   "Internship", "Daily Wage", "Unemployed"]


@router.route('/users', methods=['GET'])
def get_users():
    from models import Sample
    number_of_users = 100  # Number of users to retrieve
    api_endpoint = f'https://randomuser.me/api/?results={number_of_users}'

    response = requests.get(api_endpoint)
    data = response.json()

    for result in data['results']:
        sample = {
            'gender': result['gender'],
            'nationality': result['nat'],
            # couldn't find api with employement_type so using a random data
            'employement_type': random.choice(employment_type),
            'age': result['dob']['age']
        }
        new_sample = Sample(gender=sample['gender'], nationality=sample['nationality'],
                            employment_type=sample['employement_type'], age=sample['age'])  # add the new user to the db
        db.session.add(new_sample)
        db.session.commit()
    return get_records()
