import os
import jwt
import datetime
from dotenv import load_dotenv
load_dotenv()


def to_json_list(list_obj):
    arr = []
    for i in list_obj:
        arr.append(i.to_json())
    return arr


def generate_user_payload(obj):
    data = {
        "id": obj.id,
        "username": obj.username,
        "email": obj.email,
        "last_login": str(obj.last_login)
    }
    obj.last_login = datetime.datetime.now()
    obj.save()
    return data


def jwt_creator(payload):
    return jwt.encode(payload, os.getenv(
        "JWT_SECRET"), algorithm="HS256")


def jwt_verifier(jwt_token):
    return jwt.decode(jwt_token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
