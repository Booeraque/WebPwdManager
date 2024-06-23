from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # MongoDB localhost connection
db = client['password_manager']
users_collection = db['users']
passwords_collection = db['passwords']


def register_user(username, password, name, email):
    hashed_password = generate_password_hash(password)
    result = users_collection.insert_one({
        'username': username,
        'password': hashed_password,
        'name': name,
        'email': email,
        'passwords': []  # Initialize an empty list for passwords
    })
    return result.inserted_id


def check_user(username, password):
    user = get_user(username)
    if user and check_password_hash(user['password'], password):
        return True
    return False


# Function to store a password for a user
def add_password(user_id, password_data):
    users_collection.update_one({'username': user_id}, {'$push': {'passwords': password_data}})


# Function to get all passwords for a user
def get_passwords(user_id):
    user = users_collection.find_one({'username': user_id})
    return user['passwords'] if user else None


def get_user(username):
    user = users_collection.find_one({'username': username})
    return user


# Function to update a password for a user

def update_password(user_id, password_id, password_data):
    users_collection.update_one(
        {'username': user_id, 'passwords.id': password_id},
        {'$set': {'passwords.$': password_data}}
    )


# Function to delete a password for a user
def delete_password(user_id, password_id):
    users_collection.update_one(
        {'username': user_id},
        {'$pull': {'passwords': {'id': password_id}}}
    )
