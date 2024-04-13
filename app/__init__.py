from flask import Flask, session
from flask_session import Session
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QWERTYUIOP'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MONGO_URI'] = 'mongodb+srv://pms:pms@pmscluster.o8rtyu8.mongodb.net/?retryWrites=true&w=majority&appName=PMSCluster'

client = MongoClient(app.config['MONGO_URI'])
db = client.project_management_db

Session(app)

from app import routes
