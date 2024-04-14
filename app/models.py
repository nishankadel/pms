from datetime import datetime
from app import db
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password, usertype = "User"):
        self.username = username
        self.email = email
        self.usertype = usertype
        self.password_hash = generate_password_hash(password)


    @staticmethod
    def find_by_username(username):
        return db.users.find_one({'username': username})

    @staticmethod
    def find_user_id(email):
        user_document = db.users.find_one({'email': email})
        if user_document:
            return str(user_document['_id'])  # Convert ObjectId to string
        return None
    
    @staticmethod
    def find_all_users():
        return db.users.find({'usertype': "User"})
    
    @staticmethod
    def userCount():
        users = db.users.find({})
        userCount = users.count()
        return userCount
    
    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def delete_by_id(user_id):
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count
    
    @staticmethod
    def find_by_email(email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                usertype=user_data['usertype']
            )
            
    def save(self):
        db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'usertype': self.usertype,
            'password': self.password_hash,
        })

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Feedback:
    def __init__(self, fullname, email, phonenumber, subject, message):
        self.fullname = fullname
        self.email = email
        self.phonenumber = phonenumber
        self.subject = subject
        self.message = message
    
    def save(self):
        db.feedbacks.insert_one({
            'fullname': self.fullname,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'subject': self.subject,
            'message': self.message,
        })
    
    @staticmethod
    def find_all_feedback():
        return db.feedbacks.find({})

    @staticmethod
    def feedbackCount():
        feedbacks = db.feedbacks.find({})
        feedbackCount = feedbacks.count()
        return feedbackCount
    
    
    @staticmethod
    def delete_by_id(feedback_id):
        result = db.feedbacks.delete_one({'_id': ObjectId(feedback_id)})
        return result.deleted_count

    
class Project:
    def __init__(self, user_id, project_title, project_description, project_task=None, collaborator=None):
        self.user_id = user_id
        self.project_title = project_title
        self.project_description = project_description
        self.project_task = project_task or []
        self.collaborator = collaborator or []

    def save(self):
        # Insert the project into the 'projects' collection
        db.projects.insert_one(self.to_dict())

    @staticmethod
    def find_by_user(user_id):
        # Find projects belonging to a specific user by user_id
        projects = db.projects.find({'user_id': user_id})
        return projects
    
    @staticmethod
    def find_one_project(project_id):
        # Find projects belonging to a specific user by user_id
        projects = db.projects.find_one({'_id': project_id})
        return projects
    

    def to_dict(self):
        return {
            'user_id':self.user_id,
            'collaborator': [{'userId': c['userId']} for c in self.collaborator],
            'projectTitle': self.project_title,
            'projectDescription': self.project_description,
            'projectTask': [{'taskName': t['taskName'], 'taskStatus': t['taskStatus']} for t in self.project_task],
        }

    @staticmethod
    def from_dict(data):
        return Project(
            user_id=data['user_id'],
            project_title=data['projectTitle'],
            project_description=data['projectDescription'],
            project_task=data.get('projectTask', []),
            collaborator=data.get('collaborator', []),
        )