import os
from datetime import timedelta
from flask import Flask, request,jsonify,make_response,Blueprint
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from dotenv import load_dotenv
# import secrets
from flask_jwt_extended import jwt_manager,JWTManager

load_dotenv()
app = Flask(__name__)
api = Api(app)
app.config["JWT_SECRET_KEY"] = "amit"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
jwtNew = JWTManager(app)
mongo = PyMongo(app)