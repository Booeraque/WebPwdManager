from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # MongoDB localhost connection
db = client['password_manager']
users_collection = db['users']
passwords_collection = db['passwords']


# Function to register a new user
def register_user(username, password):
    hashed_password = generate_password_hash(password)
    result = users_collection.insert_one({'username': username, 'password': hashed_password})
    return result.inserted_id


# Function to store a password for a user
def store_password(user_id, password_data):
    password_data['user_id'] = user_id
    result = passwords_collection.insert_one(password_data)
    return result.inserted_id


# Function to get all passwords for a user
def get_passwords(user_id):
    passwords = passwords_collection.find({'user_id': user_id})
    return list(passwords)


# Function to update a password for a user
def update_password(user_id, password_id, password_data):
    passwords_collection.update_one({'_id': password_id, 'user_id': user_id}, {'$set': password_data})


# Function to delete a password for a user
def delete_password(user_id, password_id):
    passwords_collection.delete_one({'_id': password_id, 'user_id': user_id})
