from flask_restplus import Resource, Namespace
import flask
from eshiBlood.models.models import UserCredential, User, UserRole
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
import flask
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
from sqlalchemy import exc
from eshiBlood.utils.role_jwt import *




donor_auth_ns = Namespace('auth-donor')
#************************************************** DONOR auth begin ******************************************************
@donor_auth_ns.route('/login')
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



@donor_auth_ns.route('/register')
class UserRegisterResource(Resource):
    @donor_auth_ns.expect(user)
    def post(self):
        payload = api.payload
        newUser = User(
            FirstName=payload["FirstName"],
            LastName=payload["LastName"],
            UserName=payload["UserName"],
            BirthDate=payload["BirthDate"],
            # is deleted
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            Gender=payload["Gender"],
            MartialStatus=payload["MaritalStatus"],
        )
        userRole = UserRole.query.filter_by(RoleName="Donor").first()
        userRole.Users.append(newUser)

        newCredential = UserCredential(
            Email=payload["Email"],
            Password=payload["Password"]
        )
        newCredential.User = newUser
        print(payload)

        # newUserRole = UserRole

        try:
            db.session.add(newCredential)
            db.session.commit()
        except exc.IntegrityError:
            pass

#************************************************** DONOR auth end ******************************************************
