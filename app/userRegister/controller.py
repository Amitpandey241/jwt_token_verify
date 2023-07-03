from app import mongo

def insert_user(user_detail):
    try:
        """here query_to_insert_user_in_db.acknowledged gives
           status which is boolean value.
         """
        email = user_detail['email']
        # print(email)
        find_email= mongo.db.users.find_one({'email':email})
        print("This is find",find_email)
        # print(find_email)
        if not find_email:
            status=mongo.db.users.insert_one(user_detail)

            result = True if status.acknowledged else False
            return result
        else:
            return False
    except Exception as e:
        return str(e)

"""This code is to test insert_user fucntion"""
# test_data = {"email" :"Amit pandey", "passsword": "djnfjsdnfa"}
# print(insert_user(test_data))

def find_user(user_details):
    try:
        result = mongo.db.users.find_one(user_details)

        if result:
            print("True of finduser2")
            return True
        else:
            print("True of finduser2")
            return False
    except Exception as e:
        return str(e)


def find_email(email_obj):
    try:
        result = mongo.db.users.find_one(email_obj)

        if result:
            print("True of finduser2")
            return True
        else:
            print("True of finduser2")
            return False
    except Exception as e:
        return str(e)

#testing find_email
# email= {"email":"pamit1687@gmail.com"}
# print(find_email(email))

def update_is_verify(email_object):
    try:
        set_field ={"$set":{"is_verify":True}}
        query_to_update_is_verify = mongo.db.users.update_one(email_object,set_field)
        print(query_to_update_is_verify,"dfasdjngs",query_to_update_is_verify.acknowledged)
        result = True if query_to_update_is_verify.acknowledged else False
        return result
    except Exception as e:
        return str(e)
# email = {"username":"Amit"}
# update_field = {"is_verify":True}
# print(update_is_verify(email,update_field))
