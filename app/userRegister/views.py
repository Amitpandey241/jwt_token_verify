from flask import Flask, make_response,jsonify,request,Blueprint
from flask_restful import Resource,Api
from app.userRegister.controller import insert_user,find_user,find_email,update_is_verify
from app.userRegister.verification import Verification,emailVerification
from app import api
from app import mail
from flask_mail import Message
import jwt
from datetime import datetime,timedelta


example_blueprint = Blueprint("example_blueprint",__name__)


class UserRegistration(Resource):
    def post(self):
        try:
            email = request.json.get("email","NA")
            password = request.json.get("password","NA")
            print("This is line 16",email,password)
            # role = request.json.get("role",False)
            # is_verify = request.json.get("is_verify",False)


            # Checking if email/password  is empty
            verify_obj = Verification()
            result = verify_obj.verify_email_password(email,password)
            if result != "Valid email password":


                return make_response(jsonify({"message":result}))

            #checking if emailid entred is correct
            object_of_email_verification = emailVerification()
            result_of_valid_email =object_of_email_verification.verfy_email(email)
            if not result_of_valid_email:
                return make_response(jsonify({"message":"Invalid Email"}))
            ######################################

            details_of_user = {"email": email, "password": password, "role": "admin", "is_verify": False}

            results = insert_user(details_of_user)
            print("This is of views results status: ",results)
            """Setting expire time for verification tokken """
            expire_token_time = datetime.now() + timedelta(minutes=15)
            expire_epoch_time = int(expire_token_time.timestamp())
            details_to_make_jwt_tokken = {"email": email , "exp":expire_epoch_time}

            veryfication_tokken = jwt.encode(details_to_make_jwt_tokken,"amit",algorithm="HS256")


            if results == True:
                print("line1")
                msg = Message('Testing', sender='ap7788546@gmail.com', recipients=[email])
                print("line2")
                msg.body = f"This is your verification Token: {veryfication_tokken}"
                print("line3")
                mail.send(msg)
                print("line4")
                return make_response(jsonify({"message":"please check your mail for verification tokken"}))
            return make_response(jsonify({"message":"Partial"}))
            ######################################
        except Exception as e:
            return make_response(jsonify({"message":f"str{e}"}))

class verifyEmail(Resource):

    def post(self):
        try:
            # token = request.json.get('token')
            token = request.headers.get('token')
            if token in ["NA",""]:
                return make_response(jsonify({"message":"Yon have not entred your token"}))
            # veryfication_tokken = jwt.encode(details_to_make_jwt_tokken,"amit",algorithm="HS256")

            decrpt_token = jwt.decode(token,"amit",algorithms=["HS256"])
            data_for_query = {"email":decrpt_token['email']}
            result_of_find = find_email(data_for_query)
            if result_of_find == True:
                update_query = update_is_verify(data_for_query)
                try:
                    if update_query:
                        return make_response(jsonify({"message":"Sucessful Verified!"}))
                    else:
                        return make_response(jsonify({"message":"Failed to update"}))
                except Exception as e:
                    return make_response(jsonify({"message":str(e)}))

        except Exception as e:
            return str(e)
class Login(Resource):
    def post(self):


api.add_resource(UserRegistration, '/')
api.add_resource(verifyEmail,'/verifyEmail')

