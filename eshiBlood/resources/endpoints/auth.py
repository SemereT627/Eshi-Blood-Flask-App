from flask_restplus import Resource, Namespace
import flask
from eshiBlood.models.models import *
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
import flask
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
from sqlalchemy import exc
from eshiBlood.utils.role_jwt import *

superadmin_ns = Namespace("superadmin")

@superadmin_ns.route('/login/')
class SuperAdminLoginResource(Resource):
    
    
    def post(self):
        data = api.payload
        print("****************super-admin-login****************")
        
        if data['Email'] != "" and data['Password'] != "":
            # Finding a user from user credential table
            userCredential = UserCredential.query.filter_by(
                Email=data['Email']).first()
                # If user credential is there
            if userCredential:
                user = User.query.filter_by(
                    UserCredential=userCredential.UserCredentialId
                ).first()
            else:
                return {"message":"user not found"}
            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            if userCredential and data['Password'] == userCredential.Password:
                roleStr = role.RoleName.value
                # tok = str(setToken(user.UserId,roleStr),'utf-8')
                # print(setToken(user.UserId,roleStr))
                # return {"x":"y"}
                response = flask.make_response()
                response.status_code = 200
                tokenValue = setToken(user.UserId,roleStr)
                # response.set_cookie("token",value = tokenValue,expires=10000000000,httponly=True)
                print(tokenValue)
                # print(f"{userCredential.Password} {data['Password'] == userCredential.Password}")
                response.set_cookie(key="token",value = tokenValue,expires=10000000000,httponly=True)
                return response
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "Email or password cannot be empty"}, 400     

@superadmin_ns.route("/invite-admin")
class SuperAdminInviteResource(Resource):
    @role_required("SuperAdmin")
    def get(self):
        return flask.request.host_url+"auth-admin"+"/register/"+setInviteToken("Admin")








#************************************************** DONOR auth begin ******************************************************
donor_auth_ns = Namespace('auth-donor')
@donor_auth_ns.route('/login/')
class UserLoginResource(Resource):
    
    @donor_auth_ns.expect(userCredential)
    def post(self):
        data = api.payload
        # print("**************** auth-donor-login")
        
        if data['Email'] != "" and data['Password'] != "":
            # Finding a user from user credential table
            userCredential = UserCredential.query.filter_by(
                Email=data['Email']).first()
            # If user credential is there
            if userCredential:
                user = User.query.filter_by(
                    UserCredential=userCredential.UserCredentialId
                ).first()
            else:
                return {"message": "user not found"}
            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            
            if userCredential and data['Password'] == userCredential.Password:
                if not userIsDeleted(user.UserId):
                    roleStr = str(role.RoleName).split('.')[-1]
                    
                    response = flask.make_response()
                    response.status_code = 200
                    tokenValue = setToken(user.UserId,roleStr)
                    
                    response.set_cookie(key="token",value = tokenValue,expires=10000000000,httponly=True)
                    return response
                else:
                    return "unauthorized", 400
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "Email or password cannot be empty"}, 400

    @role_required('Donor')
    def get(self):
        print(getTokenUserId(self.token))
        return {"Message": "You are Logged In"}



@donor_auth_ns.route('/register/')
class UserRegisterResource(Resource):
    @donor_auth_ns.expect(user)
    def post(self):
        payload = api.payload
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        newUser = User()
        newUser.FirstName = payload["FirstName"]
        newUser.LastName = payload["LastName"]
        newUser.UserName = payload["UserName"]
        newUser.Gender = payload["Gender"]
        newUser.BirthDate = payload["BirthDate"]
        newUser.CreatedAt = datetime.datetime.now()
        newUser.UpdatedAt = datetime.datetime.now()
        newUser.MartialStatus = payload["MartialStatus"]
        queriedBloodType = BloodType.query.filter_by(BloodTypeName=payload["BloodType"]).first()
        queriedBloodType.Users.append(newUser)
        
        newAddress = Address()
        newAddress.State = payload["State"]
        newAddress.Zone = payload["Zone"]
        newAddress.Woreda = payload["Woreda"]
        newAddress.PhoneNumber = payload["PhoneNumber"]

        newAddress.User = newUser
        
        newCredential = UserCredential()
        newCredential.Email = payload["Email"]
        newCredential.Password = payload["Password"]

        newCredential.User = newUser

        queriedRole = UserRole.query.filter_by(RoleName="Donor").first()
        queriedRole.Users.append(newUser)

        db.session.add_all([newUser,newAddress,newCredential])
        db.session.commit()
        return {"msg":"user created"}

########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

admin_auth_ns = Namespace("auth-admin")

#************************************************** ADMIN auth begin ******************************************************
# @admin_auth_ns.route('/login')
# class UserLoginResource(Resource):
    
#     @admin_auth_ns.expect(userCredential)
#     def post(self):
#         data = api.payload
#         print("****************auth-admin-login****************")
        
#         if data['Email'] != "" and data['Password'] != "":
#             # Finding a user from user credential table
#             userCredential = UserCredential.query.filter_by(
#                 Email=data['Email']).first()
#                 # If user credential is there
#             if userCredential:
#                 user = User.query.filter_by(
#                     UserCredential=userCredential.UserCredentialId
#                 ).first()
#             else:
#                 return {"message":"user not found"}
#             role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
#             if userCredential and data['Password'] == userCredential.Password:
#                 roleStr = str(role.RoleName).split('.')[-1]
                
#                 response = flask.make_response()
#                 response.status_code = 200
#                 tokenValue = setToken(user.UserId,roleStr)
                
#                 print(tokenValue)
                
#                 response.set_cookie(key="token",value = tokenValue,expires=10000000000,httponly=True)
#                 return response
#             else:
#                 return {"message": "Email or password incorrect"}, 400

#         return {"message": "Email or password cannot be empty"}, 400     
# 
    # @role_required('Admin')
    # def get(self):
    #     return {"Message":"You are Logged In"}
# @invitation_required("Admin")
@admin_auth_ns.route('/register/')
class UserRegisterResource(Resource):
    @admin_auth_ns.expect(user)
    # @invitation_required("Admin")
    def post(self):
        db.session.rollback()
        payload = api.payload
        payload = api.payload
        # token = request.headers.get("token")
        # uid = getTokenUserId(token)
        newUser = User()
        print(payload)
        newUser.FirstName = payload["FirstName"]
        newUser.LastName = payload["LastName"]
        newUser.UserName = payload["UserName"]
        newUser.Gender = payload["Gender"]
        newUser.BirthDate = payload["BirthDate"]
        newUser.CreatedAt = datetime.datetime.now()
        newUser.UpdatedAt = datetime.datetime.now()
        newUser.MartialStatus = payload["MartialStatus"]
        queriedBloodType = BloodType.query.filter_by(BloodTypeName=payload["BloodType"]).first()
        queriedBloodType.Users.append(newUser)
        
        newAddress = Address()
        newAddress.State = payload["State"]
        newAddress.Zone = payload["Zone"]
        newAddress.Woreda = payload["Woreda"]
        newAddress.PhoneNumber = payload["PhoneNumber"]

        newAddress.User = newUser
        
        newCredential = UserCredential()
        newCredential.Email = payload["Email"]
        newCredential.Password = payload["Password"]

        newCredential.User = newUser

        queriedRole = UserRole.query.filter_by(RoleName="Admin").first()
        queriedRole.Users.append(newUser)

        db.session.add_all([newUser,newAddress,newCredential])
        db.session.commit()
        return {"msg":"user created"}
        # return userSchema.dump(newUser)
        # return {"msg":"unauthorized access"}

#************************************************** ADMIN auth end ******************************************************
#************************************************** ADMIN auth end ******************************************************
#************************************************** ADMIN auth end ******************************************************


auth_ns = Namespace("")
#************************************************** Nurse auth begin ******************************************************

@auth_ns.route('/login/')
class UserLoginResource(Resource):
    
    @auth_ns.expect(userCredential)
    def post(self):
        data = api.payload
        print("***************** auth-nurse-login")
        
        if data['Email'] != "" and data['Password'] != "":
            # Finding a user from user credential table
            userCredential = UserCredential.query.filter_by(
                Email=data['Email']).first()
                # If user credential is there
            if userCredential:
                user = User.query.filter_by(
                    UserCredential=userCredential.UserCredentialId
                ).first()
            else:
                return {"message":"user not found"}
            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            if userCredential and data['Password'] == userCredential.Password:
                roleStr = str(role.RoleName).split('.')[-1]
                # tok = str(setToken(user.UserId,roleStr),'utf-8')
                # print(setToken(user.UserId,roleStr))
                # return {"x":"y"}
                tokenValue = setToken(user.UserId,roleStr)
                response = flask.make_response({"role":role.RoleName.value,"token":tokenValue})
                response.status_code = 200
                
                # response.set_cookie("token",value = tokenValue,expires=10000000000,httponly=True)
                print(tokenValue)
                # print(f"{userCredential.Password} {data['Password'] == userCredential.Password}")
                # response.set_cookie(key="token",value = tokenValue,expires=10000000000,httponly=True)
                
                return response
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "Email or password cannot be empty"}, 400    

@auth_ns.route('/register/')
class UserRegisterResource(Resource):
    @admin_auth_ns.expect(user)
    # @invitation_required("Admin")
    def post(self):
        db.session.rollback()
        payload = api.payload
        payload = api.payload
        # token = request.headers.get("token")
        # uid = getTokenUserId(token)
        newUser = User()
        print(payload)
        newUser.FirstName = payload["FirstName"]
        newUser.LastName = payload["LastName"]
        newUser.UserName = payload["UserName"]
        newUser.Gender = payload["Gender"]
        newUser.BirthDate = payload["BirthDate"]
        newUser.CreatedAt = datetime.datetime.now()
        newUser.UpdatedAt = datetime.datetime.now()
        newUser.MartialStatus = payload["MartialStatus"]
        queriedBloodType = BloodType.query.filter_by(BloodTypeName=payload["BloodType"]).first()
        queriedBloodType.Users.append(newUser)
        
        newAddress = Address()
        newAddress.State = payload["State"]
        newAddress.Zone = payload["Zone"]
        newAddress.Woreda = payload["Woreda"]
        newAddress.PhoneNumber = payload["PhoneNumber"]

        newAddress.User = newUser
        
        newCredential = UserCredential()
        newCredential.Email = payload["Email"]
        newCredential.Password = payload["Password"]

        newCredential.User = newUser

        queriedRole = UserRole.query.filter_by(RoleName="Donor").first()
        queriedRole.Users.append(newUser)

        db.session.add_all([newUser,newAddress,newCredential])
        db.session.commit()
        return {"msg":"user created"}    

# @auth_ns.route('/register')
# class UserRegisterResource(Resource):
#     @auth_ns.expect(user)
#     def post(self):
#         payload = api.payload
#         newRegisteredUser = payload
#         newUser = User(
#             FirstName=newRegisteredUser["FirstName"], 
#             LastName=newRegisteredUser["LastName"], 
#             UserName=newRegisteredUser["UserName"], 
#             BirthDate=newRegisteredUser["BirthDate"],
#             # is deleted
#             CreatedAt=datetime.utcnow(),
#             UpdatedAt=datetime.utcnow(),
#             Gender=newRegisteredUser["Gender"],
#             MartialStatus=newRegisteredUser["MaritalStatus"], 
#             )
#         userRole = UserRole.query.filter_by(RoleName="Nurse").first()
#         userRole.Users.append(newUser)

#         newUserCredential = payload
#         newCredential = UserCredential(
#             Email=newUserCredential["Email"],
#             Password=newUserCredential["Password"]
#         )
#         newCredential.User = newUser
#         print(newUserCredential)
        
#         # newUserRole = UserRole
        
        
#         db.session.add(newCredential)
#         db.session.commit()

#         print(newUser)
#         db.session.add(newUser)
#         db.session.commit()
#         return userSchema.dump(newUser)
#************************************************** Nurse auth end ******************************************************
#************************************************** Nurse auth end ******************************************************
#************************************************** Nurse auth end ******************************************************
