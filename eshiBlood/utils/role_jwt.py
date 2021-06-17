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
from eshiBlood.models.models import UserRole, User, UserCredential
# from eshiBlood.forms.forms import LoginForm, SignUpForm
# from eshiBlood.models.models2 import *
load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def role_required(roleArg):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get("token")
            print(f"headers {token}")

            if not token:

                return jsonify({'message': 'Token is missing!'})
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                # print(data["role"]+"#################")
                if data["role"] == roleArg and not userIsDeleted(getTokenUserId(token)):
                    print(data["role"]+"****************")
                else:
                    return jsonify(msg="Unauthorized personnel")
            except:
                return jsonify(msg='Token is invalid!')
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def getTokenUserId(token):
    token = request.headers.get("token")
    print(f"headers {token}")
    data = jwt.decode(token, app.config['SECRET_KEY'])
    return data["id"]

def userIsDeleted(id):
    print("user is deleted function accessed")
    try:
        
        queriedUser = User.query.filter_by(UserId=id).first()
        if str(queriedUser.IsDeleted) == "1":
            print(f"true deleted{queriedUser.IsDeleted}")
            return True
        else:
            return False
    except:
        return True
def tokenRole():
    token = request.headers.get("token")
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except:
        pass
    data = jwt.decode(token, app.config['SECRET_KEY'])
    return data["role"]
    


def setToken(id, role):
    token = str(jwt.encode({'id': id, "role": role, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(seconds=10000000005)}, app.config['SECRET_KEY']), "utf-8")
    return token


def unsetToken():
    return ""


def either_roles_required(*roleArgs):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = request.headers.get("token")
            print(f"headers {token}")

            if not token:

                return jsonify({'message': 'Token is missing!'})
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                print(data["role"])
                if data["role"] in roleArgs  and not userIsDeleted(getTokenUserId(token)):
                    print(data["role"])
                else:
                    return jsonify(msg="Unauthorized personnel")
            except:
                return jsonify(msg='Token is invalid!')
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def invitation_required(invitedAs):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # token = request.args.get("token")
            # token = request.headers.get("token")
            invitation_token = request.args.get("invitation_token")
            print(f"headers {invitation_token}")

            if (invitation_token != None or invitation_token != ""):

                return jsonify({'message': 'Token is missing!'})
            try:
                # print("*************" +str(jwt.decode(token,'my_secret_key')))
                data = jwt.decode(invitation_token, app.config['SECRET_KEY'])
                print(data["invitation-token"])
                if data["invitation-token"] == invitedAs:
                    # work db ops
                    print(data["invitation-token"])
                else:
                    return jsonify(msg="Unauthorized personnel")
            except:
                return jsonify(msg='Token is invalid!')
            return fn(*args, **kwargs)

        return decorator

    return wrapper

# decrease exp time to 15 minutes
def setInviteToken(invitedAs):
    token = str(jwt.encode({"invitation-token": invitedAs, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(seconds=(1000000))}, app.config['SECRET_KEY']), "utf-8")
    return token


def isValidInviteToken(inviteToken):
    """isValidInviteToken

    Keyword arguments:
    inviteToken -- string of token from cookie
    Return: Boolean
    """

    try:
        jwt.decode(inviteToken, app.config["SECRET_KEY"])
        return True
    except:
        return False
