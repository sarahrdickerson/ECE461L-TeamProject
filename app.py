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
import os

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')
mongo = PyMongo(
    app, uri='mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Users')
mongo_projects = PyMongo(
    app, uri='mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/Projects')
mongo_HWSet = PyMongo(
    app, uri='mongodb+srv://gabrielaperezgil:ECE461L@cluster0.5v3hp19.mongodb.net/HWSets')

# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/api/project-authorized-users', methods=['POST'])
def return_project_authorized_users():
    project_data = request.get_json()
    project_name = project_data['project_name']
    project_id = project_data['project_id']

    projects_collection = mongo_projects.db[project_id]
    project_document = projects_collection.find_one({})
    authorized_users = project_document['users']
    print(authorized_users)
    return jsonify({"success": True, "authorized_users": authorized_users})



@app.route('/api/availability')
def get_availability():
    HWSet1_collection = mongo_HWSet.db['HWSet1']
    HWSet1_document = HWSet1_collection.find_one({})
    HWSet1_curr_available = HWSet1_document['available']

    HWSet2_collection = mongo_HWSet.db['HWSet2']
    HWSet2_document = HWSet2_collection.find_one({})
    HWSet2_curr_available = HWSet2_document['available']
    return jsonify({
        "success": True,
        "HWSet1_available": HWSet1_curr_available,
        "HWSet2_available": HWSet2_curr_available})


@app.route('/api/checkin_HWSet1', methods=['POST'])
def checkin_HWSet1():
    HWSet1_data = request.get_json()
    qty = int(HWSet1_data['qty'])
    if(qty <= 0):
        return jsonify({"success": False, "message": "invalid value"})
    collection = mongo_HWSet.db['HWSet1']
    document = collection.find_one({})
    current_availability = int(document['available'])
    current_capacity = int(document['capacity'])

    if (qty > (current_capacity - current_availability)):
        return jsonify({"success": False, "message": "qty checked in exceeds capacity"})
    else:
        # does not exceed can proceed and update availability
        collection.update_one(
            {}, {'$set': {'available': qty + current_availability}})
        return jsonify({"success": True, "message": "hardware has been checked in"})


@app.route('/api/checkout_HWSet1', methods=['POST'])
def checkout_HWSet1():
    HWSet1_data = request.get_json()
    qty = int(HWSet1_data['qty'])
    if(qty <= 0):
        return jsonify({"success": False, "message": "invalid value"})
    collection = mongo_HWSet.db['HWSet1']
    document = collection.find_one({})
    current_availability = int(document['available'])

    if (qty > (current_availability)):
        return jsonify({"success": False, "message": "qty checked out exceeds available hardware"})
    else:
        # does not exceed can proceed and update availability
        collection.update_one(
            {}, {'$set': {'available': current_availability - qty}})
        return jsonify({"success": True, "message": "hardware has been checked out"})


@app.route('/api/checkin_HWSet2', methods=['POST'])
def checkin_HWSet2():
    HWSet2_data = request.get_json()
    qty = int(HWSet2_data['qty'])
    if(qty <= 0):
        return jsonify({"success": False, "message": "invalid value"})
    collection = mongo_HWSet.db['HWSet2']
    document = collection.find_one({})
    current_availability = int(document['available'])
    current_capacity = int(document['capacity'])

    if (qty > (current_capacity - current_availability)):
        return jsonify({"success": False, "message": "qty checked in exceeds capacity"})
    else:
        # does not exceed can proceed and update availability
        collection.update_one(
            {}, {'$set': {'available': qty + current_availability}})
        return jsonify({"success": True, "message": "hardware has been checked in"})


@app.route('/api/checkout_HWSet2', methods=['POST'])
def checkout_HWSet2():
    HWSet2_data = request.get_json()
    qty = int(HWSet2_data['qty'])
    if(qty <= 0):
        return jsonify({"success": False, "message": "invalid value"})
    collection = mongo_HWSet.db['HWSet2']
    document = collection.find_one({})
    current_availability = int(document['available'])

    if (qty > (current_availability)):
        return jsonify({"success": False, "message": "qty checked out exceeds available hardware"})
    else:
        # does not exceed can proceed and update availability
        collection.update_one(
            {}, {'$set': {'available': current_availability - qty}})
        return jsonify({"success": True, "message": "hardware has been checked out"})

# HW set1 get availability


@app.route('/api/get_HWSet1')
def get_avail_HWSet1():
    collection = mongo_HWSet.db.HWSet1
    data = []

    for document in collection.find():
        data.append(
            {'availability_HWSet1': document['available'], 'capacity_HWSet1 ': 100})
    return jsonify(data)

# HW set1 set availability


@app.route('/api/set_HWSet1', methods=['POST'])
def set_avail_HWSet1():
    HWSet1_data = request.get_json()
    HWSet1_avail = HWSet1_data['available']
    print("Updating availability to:", HWSet1_avail)
    result = mongo_HWSet.db.HWSet1.updateOne(
        {'name': 'HWSet1'},
        {'$set': {'available': HWSet1_avail}}
    )
    print(result)
    return jsonify({"message": "Availability updated successfully"})

# join project API and adds user to project if not already in project
@app.route('/api/joinProject', methods=['POST'])
def join_project():
    project_data = request.get_json()
    project_id = project_data['project_id']
    user_id = project_data['user_id']

    if project_id in mongo_projects.db.list_collection_names():
        if user_id not in mongo_projects.db[project_id].find_one({})['users']:
            mongo_projects.db[project_id].update_one(
                {}, {'$push': {'users': user_id}})
            return jsonify({"success": True, "message": "user added to project"})
        else:
            return jsonify({"success": True, "message": "user already exists in project"})
    else:
        return jsonify({"success": False, "message": "project does not exist"})


# create project API
@app.route('/api/createProject', methods=['POST'])
def create_project():
    project_data = request.get_json()
    # example project_data
    # {"project_name": "ece319k project", "project_id":"4y7e8wt" }
    project_id = project_data['project_id']

    if project_id not in mongo_projects.db.list_collection_names():
        mongo_projects.db.create_collection(project_id)
        mongo_projects.db[project_id].insert_one(project_data)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "project id already exists"})

# this is a simple API that returns User Information data
# this will be called by the react front end
@app.route('/userdata')
def get_user_data():
    collection = mongo.db.abhaysamant
    data = []

    for document in collection.find():
        data.append(
            {'userid is': document['userid'], 'password is': document['password']})
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


# api for removing a user from database
# NOTE: not password protected, so anyone can remove a user without their password
@app.route('/api/remove_user', methods=['POST'])
def remove_user():
    # get username
    username = request.get_json()['username']

    # check if username exists in database
    if username in mongo.db.list_collection_names():
        # remove user from database
        mongo.db.drop_collection(username)
        return jsonify({"success": True, "message": "User " + str(username) + " removed"})
    else:
        return jsonify({"success": False, "message": "User does not exist"})

# api for logging in users


@app.route('/api/login', methods=['POST'])
def login():
    # get login data
    print("hello im here!")
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


# if __name__ == '__main__':
#     app.run(port=8000, debug=True)