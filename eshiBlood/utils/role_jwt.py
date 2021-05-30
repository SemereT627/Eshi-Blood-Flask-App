import os
import datetime
from functools import wraps
from flask import url_for, flash, redirect, Flask, jsonify, request, make_response
from flask import request, make_response
import jwt
import datetime
from functools import wraps
# custom imports
from eshiBlood import app
from dotenv import load_dotenv
from eshiBlood.models.models import UserRole,User,UserCredential
# from eshiBlood.forms.forms import LoginForm, SignUpForm
# from eshiBlood.models.models2 import *
load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def role_required(roleArg):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.args.get("token")

            if not token:

                return jsonify({'message': 'Token is missing!'})
            try:
                # print("*************" +str(jwt.decode(token,'my_secret_key')))
                data = jwt.decode(token, app.config['SECRET_KEY'])
                print(data["role"])
                if data["role"] == roleArg:
                    # work db ops
                    print(data["role"])
                else:
                    return jsonify(msg="Unauthorized personnel")
            except:
                return jsonify(msg='Token is invalid!')
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def getTokenUserId(req):
    token = req.args.get("token")
    data = jwt.decode(token, app.config['SECRET_KEY'])
    return data["id"]

def setToken(id,role):
    token = str(jwt.encode({'id': id, "role": role, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']), "utf-8")# perform crud and assign id and role after finishing registration >> token to be saved in session storage
    return {"token":token}



# @app.route("/login",methods=["POST"])
# def login():
    # token = str(jwt.encode({'id':'1',"role":"Admin", 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']),"utf-8")
    # return jsonify(token=token)


# def register():
    # password = request.form["password"]
    # form input
    # form validate
    # database create
    # query roles
    # print(password+"-------------------------------")
    # if(password == "password"):
    #     token = str(jwt.encode({'id': '1', "role": "User", 'exp': datetime.datetime.utcnow(
    #     ) + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']), "utf-8")# perform crud and assign id and role after finishing registration >> token to be saved in session storage
    #     return jsonify(token=token)
    # return "invalid password"



# @role_required("Admin")  # Admin role only
# def adminPage():
#     return "Accessible by Admin only"


# @role_required("User")  # User role only
# def userPage():
#     print(getTokenUserId(request)+"qqqqqqqqqqqqqqqqqqqq")
#     return "Accessible by User only"
