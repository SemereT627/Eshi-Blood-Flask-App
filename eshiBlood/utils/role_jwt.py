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
            token = request.cookies.get("token")
            print(f"cookies {token}")

            if not token:

                return jsonify({'message': 'Token is missing!'})
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                print(data["role"])
                if data["role"] == roleArg:
                    print(data["role"])
                else:
                    return jsonify(msg="Unauthorized personnel")
            except:
                return jsonify(msg='Token is invalid!')
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def getTokenUserId(req):
    token = request.cookies.get("token")
    print(f"cookies {token}")
    data = jwt.decode(token, app.config['SECRET_KEY'])
    return data["id"]

def setToken(id,role):
    token = str(jwt.encode({'id': id, "role": role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1005)}, app.config['SECRET_KEY']), "utf-8")    
    return token

def unsetToken():
    return ""



