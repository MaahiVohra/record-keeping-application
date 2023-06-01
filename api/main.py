from flask import Blueprint, jsonify, make_response
import requests
import random

from __init__ import create_app, db
main = Blueprint('main', __name__)

employment_type = ["Full-time", "Part-time",
                   "Internship", "Daily Wage", "Unemployed"]


@main.route('/')  # home page for the api server
def index():
    return "Hello from the login-api"


@main.route('/users', methods=['GET'])
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
    return make_response(jsonify({'message': "Sample Increases"}), 200)


app = create_app()
if __name__ == '__main__':  # ensures it only runs when the script is executed not when used as a module
    with app.app_context():  # establishes application context
        db.create_all()  # creates tables inside the database according to the models
    app.run(debug=True)
