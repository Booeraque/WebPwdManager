from flask import Flask, render_template, request, session, redirect

from PwdManager.SourceCode.mongodb import (register_user, add_password,
                                           get_passwords, update_password, delete_password,
                                           check_user)

from PwdManager.SourceCode.PasswordGenerator import PasswordGenerator

app = Flask(__name__)
app.secret_key = 'your secret key'  # replace with your secret key


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['register--username']
        password = request.form['register--password']
        name = request.form['register--name']
        email = request.form['register--email']
        user_id = register_user(username, password, name, email)
        if user_id:
            return redirect('/login')
        else:
            return render_template("register.html", error_message="Username already exists")
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login--username']
        password = request.form['login--password']
        if check_user(username, password):
            session['username'] = username
            return render_template('dashboard.html', user=username, username=session['username'])
        else:
            return render_template('login.html', error_message="Invalid username or password")
    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return render_template('login.html')


@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    password_options = request.get_json()
    length = password_options.get('length', '8')  # Default length is 8 if not provided
    length = int(length) if length.isdigit() else 8
    use_uppercase = password_options.get('useUppercase', False)
    use_numbers = password_options.get('useNumbers', False)
    use_symbols = password_options.get('useSymbols', False)

    password_generator = PasswordGenerator(length, use_uppercase, use_numbers, use_symbols)
    password = password_generator.generate_password()

    return {'password': password}, 200


@app.route('/save_pass', methods=['POST'])
def save_password_route():
    user_id = session['username']
    password_data = request.get_json()
    password_id = add_password(user_id, password_data)
    if password_id:
        return {'message': 'Saved'}, 200
    else:
        return {'message': 'Error'}, 500


@app.route('/get_pass', methods=['GET'])
def get_passwords_route():
    user_id = session['username']
    passwords = get_passwords(user_id)
    return {"passwords": passwords}, 200


@app.route('/update_pass', methods=['POST'])
def update_password_route():
    user_id = session['username']
    password_id = request.form['password_id']
    password_data = request.get_json()
    update_password(user_id, password_id, password_data)
    return {'message': 'Updated'}, 200


@app.route('/del_pass', methods=['POST'])
def delete_password_route():
    user_id = session['username']
    password_id = request.form['password_id']
    delete_password(user_id, password_id)
    return {"message": "Deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)
