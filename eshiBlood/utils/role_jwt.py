import datetime
from functools import wraps
from flask import url_for, flash, redirect, Flask, jsonify, request, make_response
from flask import request, make_response
import jwt
import datetime
from functools import wraps
# custom imports
from eshiBlood import app
# from eshiBlood.forms.forms import LoginForm, SignUpForm
# from eshiBlood.models.models2 import *


app.config["SECRET_KEY"] = 'mysecretkey'


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.args.get("token")

            if not token:

                return jsonify({'message': 'Token is missing!'}), 403
            try:
                # print("*************" +str(jwt.decode(token,'my_secret_key')))
                data = jwt.decode(token, app.config['SECRET_KEY'])
                print(data["role"])
                if data["role"] == role:
                    # work db ops
                    print(data["role"])
                else:
                    return jsonify(msg="Admins only!"), 403
            except:
                return jsonify({'message': 'Token is invalid!'}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def getTokenUserId(req):
    token = req.args.get("token")
    data = jwt.decode(token, app.config['SECRET_KEY'])
    return data["id"]


# @app.route("/login",methods=["POST"])
# def login():
    # token = str(jwt.encode({'id':'1',"role":"Admin", 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']),"utf-8")
    # return jsonify(token=token)

@app.route("/register", methods=["POST"])
def register():
    password = request.form["password"]
    print(password+"-------------------------------")
    if(password == "password"):
        token = str(jwt.encode({'id': '1', "role": "User", 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']), "utf-8")# perform crud and assign id and role after finishing registration >> token to be saved in session storage
        return jsonify(token=token)
    return "invalid password"


@app.route("/admin", methods=["GET"])
@role_required("Admin")  # Admin role only
def adminPage():
    return "Accessible by Admin only"


@app.route("/user", methods=["GET"])
@role_required("User")  # User role only
def userPage():
    print(getTokenUserId(request)+"qqqqqqqqqqqqqqqqqqqq")
    return "Accessible by User only"
