# make sure you are in the backend folder in cmd
# create myenv or enter existing one (to enter existing one, skip to activate step)
# python -m venv myenv
# install all packages 
# pip install -r requirements.txt
# activate 
# .\myenv\Scripts\activate
# flask run --port=8000
# http://localhost:8000/userdata to see data

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Users'
mongo = PyMongo(app, uri='mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Users')
mongo1 = PyMongo(app, uri='mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Projects')


@app.route('/api/createProject', methods=['POST'])
def create_project():
    project_data = request.get_json()
    # example project_data
    # {"project_name": "ece319k project", "project_id":"4y7e8wt" }
    project_name = project_data['project_name']
    project_id = project_data['project_id']

    if project_name not in mongo1.db.list_collection_names():
        # check if project id exists already
        mongo1.db.create_collection(project_name)
        result = mongo1.db[project_name].insert_one(project_data)
        return jsonify({"success":True})
    else:
        return jsonify({"success":False, "message": "project name already exists"})


# this is a simple API that returns User Information data
# this will be called by the react front end
@app.route('/userdata')
def get_user_data():
    collection = mongo.db.abhaysamant
    data = []

    for document in collection.find():
        data.append({'userid is': document['userid'], 'password is': document['password']})
    return jsonify(data)


# api for submitting new user data
# defining the endpoint for application with HTTP method POST
@app.route('/api/submit_new_user', methods=['POST'])
def submit_new_user():
    # process user data
    user_data = request.get_json()
    # example user_data
    # {"username": "gabrielaperez","userid": gp,"password": ECE461L}
    
    # get the username, since the collection will be named after the user as shown in HW 4
    collection_name = user_data['username']
    user_id = user_data['userid']

    # double check username doesn't already exist when they're trying to create a new account
    if collection_name not in mongo.db.list_collection_names():
        # create new collection named after new user   
        mongo.db.create_collection(collection_name)
        result = mongo.db[collection_name].insert_one(user_data)
        return jsonify({"success": True, "document_id": str(result.inserted_id)})
    else:
        return jsonify({"success": False, "message": "Username already exists"})
    

# api for logging in users
@app.route('/api/login', methods=['POST'])
def login():
    # get login data
    username = request.get_json()['username']
    password = request.get_json()['password']
    userid = request.get_json()['userid']

    # check if username exists in database
    if username in mongo.db.list_collection_names():
        # check if userid matches
        if userid == mongo.db[username].find_one()['userid']:
            # check if password matches
            if password == mongo.db[username].find_one()['password']:
                return jsonify({"success": True, "message": "Login successful"})
            else:
                return jsonify({"success": False, "message": "Incorrect password"})
        else:
            # userid doesnt match
            return jsonify({"success": False, "message": "Incorrect User ID"})
    else:
        return jsonify({"success": False, "message": "Username does not exist"})


if __name__ == '__main__':
    app.run(port=8000, debug=True)


