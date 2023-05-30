from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)
etype = ["Full-time", "Part-time", "Internship", "Daily Wage", "Unemployed"]


@app.route('/users', methods=['GET'])
def get_users():
    number_of_users = 10  # Number of users to retrieve
    api_endpoint = f'https://randomuser.me/api/?results={number_of_users}'

    response = requests.get(api_endpoint)
    data = response.json()

    users = []

    for result in data['results']:
        user = {
            'gender': result['gender'],
            'nationality': result['nat'],
            'employement_type': random.choice(etype),
            'age': result['dob']['age']
        }
        users.append(user)

    return jsonify(users)


if __name__ == '__main__':
    app.run()
