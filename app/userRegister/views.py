from flask import Flask, make_response,jsonify,request,Blueprint
from flask_restful import Resource,Api
from app.userRegister.controller import insert_user,find_user,find_email,update_is_verify,find_password,find_is_active,get_role,update_age,update_isverify
from app.userRegister.verification import Verification,emailVerification
from app import api
from app import mail
from flask_mail import Message
import jwt
from datetime import datetime,timedelta
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required

example_blueprint = Blueprint("example_blueprint",__name__)


class UserRegistration(Resource):
    def post(self):
        try:
            email = request.json.get("email","NA")
            password = request.json.get("password","NA")
            print("This is line 16",email,password)
            role = request.json.get("role","admin")
            is_verify = False


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

            details_of_user = {"email": email, "password": password, "role": role, "is_verify": is_verify}

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
        try:
            email = request.json.get("email","NA")
            password = request.json.get("password","NA")
            if email in ["NA",""] or password in ["NA",""]:
                return make_response(jsonify({"message":"Please Enter Correct Mail and password"}))
            else:
                user_details = {"email":email,"password":password}
                find_user_details = find_user(user_details)
                find_user_active =find_is_active(user_details)
                if find_user_active:
                    if find_user_details:
                        find_pass=find_password(user_details)
                        if find_pass:
                            claims = {"role":get_role(user_details)}
                            access_token = create_access_token(identity=email)
                            refresh_token = create_refresh_token(identity=email)
                            return make_response(jsonify({"acces-token":access_token,"refresh-tokn":refresh_token}))

                        else:
                            return make_response(jsonify({"message":"You have Entred Incorrect Password!"}))



                    else:
                        return make_response(jsonify({"message": "Please Check your mail its and incorrect!"}))
                else:
                    return make_response(jsonify({"message":"Please verify your account!!"}))


        except Exception as e:
            return make_response(jsonify({"message":str(e)}))



class UpdateData(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user_role =get_role({"email":email})
        find_mail =find_email({"email":email})
        if user_role:
            if find_mail:
                field_to_update = request.json.get("age","NA")
                if field_to_update in ["NA",""]:
                    return make_response(jsonify({"message":"Enter value to update!"}))
                else:
                    obj_email = {"email":email}
                    obj_to_update = {"age":field_to_update}
                    result =update_age(obj_email,obj_to_update)
                    if result:
                        return make_response(jsonify({"message":"Field has been Updated!!"}))
                    else:
                        return make_response(jsonify({"message":"Field has been not updated "}))
            else:
                return make_response(jsonify({"message":"Your Email address is wrong"}))
        else:
            return make_response(jsonify({"message": "You are not allowed to update! Please update your pemissions"}))

class DeleteUser(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user_role = get_role({"email": email})
        find_mail = find_email({"email": email})
        if user_role:
            if find_mail:
                obj_email = {"email": email}
                obj_isverify = {"is_verify":False}
                result = update_isverify(obj_email,obj_isverify)
                if result:
                    return make_response(jsonify({"message": "Users has been Deleted!!"}))
                else:
                    return make_response(jsonify({"message": "Users has been not updated "}))

            else:
                return make_response(jsonify({"message": "Your Email address is wrong"}))
        else:
            return make_response(jsonify({"message": "You are not allowed to update! Please update your pemissions"}))


api.add_resource(UserRegistration, '/')
api.add_resource(verifyEmail,'/verifyEmail')
api.add_resource(Login,'/login')
api.add_resource(UpdateData,'/update')
api.add_resource(DeleteUser,'/delete')
