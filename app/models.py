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
    
    # @staticmethod
    # def userCount():
    #     users = db.users.find({})
    #     userCount = users.count()
    #     return userCount
    
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

    # @staticmethod
    # def feedbackCount():
    #     feedbacks = db.feedbacks.find({})
    #     feedbackCount = feedbacks.count()
    #     return feedbackCount
    
    
    @staticmethod
    def delete_by_id(feedback_id):
        result = db.feedbacks.delete_one({'_id': ObjectId(feedback_id)})
        return result.deleted_count

    
class Project:
    def __init__(self, userid, projecttitle, projectdescription):
        self.userid = userid
        self.projecttitle = projecttitle
        self.projectdescription = projectdescription
        

    def save(self):
        # Insert the project into the 'projects' collection
        db.projects.insert_one({
            'userid': self.userid,
            'projecttitle': self.projecttitle,
            'projectdescription': self.projectdescription,
            })
        
    @staticmethod
    def find_by_user(userid):
        # Retrieve all projects for a specific user
        projects = db.projects.find({'userid': userid})
        return list(projects)
    
    @staticmethod
    def find_project_by_id(project_id):
        # Retrieve a single project by its project ID
        try:
            project = db.projects.find_one({'_id': ObjectId(project_id)})
            if project:
                project['_id'] = str(project['_id'])  # Convert ObjectId to string
                return project
            else:
                return None  # Project not found
        except Exception as e:
            print(f"Error finding project by ID: {e}")
            return None  # Handle any exceptions gracefully
    
    @staticmethod
    def delete_project_by_id(project_id):
        # Delete a project by its project ID
        try:
            result = db.projects.delete_one({'_id': ObjectId(project_id)})
            if result.deleted_count > 0:
                return True  # Project deleted successfully
            else:
                return False  # Project not found or not deleted
        except Exception as e:
            print(f"Error deleting project by ID: {e}")
            return False  # Handle any exceptions gracefully
    
    

class Task:
    def __init__(self, projectid, tasktitle, taskstatus):
        self.projectid = projectid
        self.tasktitle = tasktitle
        self.taskstatus = taskstatus
        

    def save(self):
        # Insert the project into the 'projects' collection
        db.tasks.insert_one({
            'projectid': self.projectid,
            'tasktitle': self.tasktitle,
            'taskstatus': self.taskstatus,
            })
   
    @staticmethod
    def find_task_by_projectid(projectid):
        # Retrieve all tasks for a specific project ID
        tasks = db.tasks.find({'projectid': projectid})
        tasks_list = []
        for task in tasks:
            task['_id'] = str(task['_id'])  # Convert ObjectId to string
            tasks_list.append(task)
        return tasks_list
    
       