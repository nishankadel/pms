from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)


    @staticmethod
    def find_by_username(username):
        return db.users.find_one({'username': username})

    @staticmethod
    def find_by_email(email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(user_data['username'], user_data['email'], user_data['password'])
        return None
    def save(self):
        db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'password': self.password_hash
        })

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
