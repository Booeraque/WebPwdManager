from PwdManager.SourceCode.PasswordGenerator import PasswordGenerator
from PwdManager.SourceCode.mongodb import register_user, add_password, get_passwords, update_password, delete_password
from werkzeug.security import check_password_hash


class PasswordManager:
    def __init__(self):
        pass

    def register_user(self, username, password):
        return register_user(username, password)

    def check_user(self, username, password):
        user = get_passwords(username)
        if user and check_password_hash(user['password'], password):
            return True
        return False

    def add_password(self, user, password_data):
        return add_password(user, password_data)

    def get_passwords(self, user):
        return get_passwords(user)

    def update_password(self, user, id, password_data):
        return update_password(user, id, password_data)

    def delete_password(self, user, id):
        return delete_password(user, id)
