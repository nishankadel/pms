from flask import Flask, session
from flask_session import Session
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QWERTYUIOP'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/project_management_db'
client = MongoClient(app.config['MONGO_URI'])
db = client.project_management_db

Session(app)

from app import routes
