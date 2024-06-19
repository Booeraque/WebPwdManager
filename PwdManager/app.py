from flask import Flask, request, jsonify, render_template, session
from SourceCode.PasswordManager import PasswordManager

app = Flask(__name__)
app.secret_key = 'your secret key'  # replace with your secret key
password_manager = PasswordManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the user exists and the password is correct
    if password_manager.check_user(username, password):
        session['username'] = username
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# TODO: Make the register function work, so the user and password can be stored in the database
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or password is None:
        return jsonify({'message': 'Username and password are required'}), 400

    user_id = password_manager.register_user(username, password)
    if user_id:
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'Registration failed'}), 500


@app.route('/passwords', methods=['GET'])
def get_passwords():
    username = session.get('username')
    if username:
        passwords = password_manager.get_passwords(username)
        return jsonify(passwords)
    else:
        return jsonify({'message': 'Not logged in'}), 401


@app.route('/passwords', methods=['POST'])
def add_password():
    username = session.get('username')
    if username:
        password_data = request.form.to_dict()
        pwd_id = password_manager.add_password(username, password_data)
        return jsonify({'message': 'Password added successfully', 'id': str(pwd_id)}), 201
    else:
        return jsonify({'message': 'Not logged in'}), 401


@app.route('/passwords/<id>', methods=['PUT'])
def update_password(pwd_id):
    username = session.get('username')
    if username:
        password_data = request.get_json()
        password_manager.update_password(username, pwd_id, password_data)
        return jsonify({'message': 'Password updated successfully'}), 200
    else:
        return jsonify({'message': 'Not logged in'}), 401


@app.route('/passwords/<id>', methods=['DELETE'])
def delete_password(pwd_id):
    username = session.get('username')
    if username:
        password_manager.delete_password(username, pwd_id)
        return jsonify({'message': 'Password deleted successfully'}), 200
    else:
        return jsonify({'message': 'Not logged in'}), 401


if __name__ == '__main__':
    app.run(debug=True)
