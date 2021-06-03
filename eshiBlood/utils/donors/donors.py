from flask_restplus import Resource, Namespace
from datetime import datetime


import flask# from flask import request
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from eshiBlood.utils.role_jwt import *
from eshiBlood.schema.ma import *
from eshiBlood.resources.validators.validators import *

donors_ns = Namespace("donors")

@donors_ns.route("")
class DonorResource(Resource):
    @donors_ns.expect(user)
    def get(self):
        donorRole = UserRole.query.filter_by(RoleName="Donor").first()
        # print(str(donorRole.UserRoleId))
        users = User.query.filter_by(UserRole = donorRole.UserRoleId).all()
        # print(users[1].UpdatedAt)
        return userSchema.dump(users)
    def post(self):
        payload = api.payload
        
        newUser = User(
            FirstName=payload["FirstName"],
            LastName=payload["LastName"],
            UserName=payload["UserName"],
            BirthDate=payload["BirthDate"],
            CreatedAt=datetime.datetime.utcnow(),
            UpdatedAt=datetime.datetime.utcnow(),
            Gender=payload["Gender"],
            MartialStatus=payload["MaritalStatus"],
        )
        userRole = UserRole.query.filter_by(RoleName="Donor").first()
        userRole.Users.append(newUser)

        
        newUserCredential = UserCredential(
            Email=payload["Email"],
            Password=payload["Password"]
        )
        newUserCredential.User = newUser
        # check if email is not registered before and password is strong
        if(isValidEmail(payload["Email"]) and isValidPassword(payload["Password"])):
            db.session.rollback()
            db.session.add_all([newUser,newUserCredential])
            db.session.commit()
            return 201
        else:
            return 400


@donors_ns.route("/<int:id>")
class DonorsResourcesWithParam(Resource):
    @donors_ns.expect(user)
    def get(self,id):
        qUser = User.query.filter_by(UserId=id).first()
        return userSchema.dump([qUser])
    def put(self,id):
        db.session.rollback()
        payload = api.payload
        qUser = User.query.filter_by(UserId=id).first()
    
        qUser.FirstName=payload["FirstName"]
        qUser.LastName=payload["LastName"]
        qUser.UserName=payload["UserName"]
        qUser.BirthDate=payload["BirthDate"]
        
        qUser.UpdatedAt=datetime.datetime.utcnow()
        qUser.Gender=payload["Gender"]
        qUser.MartialStatus=payload["MaritalStatus"]

        db.session.commit()
        return 201

    def delete(self,id):
        db.session.rollback()
        qUser = User.query.filter_by(UserId=id).first()
        qUser.IsDeleted = 1
        db.session.commit()
        return 410





@donors_ns.route("/id")
class getToken(Resource):
    @role_required("Donor")
    def get(self):
        print("token**********************")
        token = flask.request.cookies.get("token")
        print(getTokenUserId(token))


    
donor_ns = Namespace("donor")


# @donor_ns.route("/appointments")
# class DonorResource(Resource):





