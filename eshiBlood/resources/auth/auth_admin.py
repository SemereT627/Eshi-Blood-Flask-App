import flask
from flask.json import jsonify
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import UserCredential, User, UserRole
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
# from flask_jwt import jwt_required
from eshiBlood.utils.role_jwt import role_required, getTokenUserId, setToken

auth_admin = Namespace('auth-admin')


@auth_admin.route('/login')
class AdminLoginResource(Resource):
    def post(self):
        payload = api.payload
        
        if payload['Email'] != "" and payload['Password'] != "":
        
            userCredential = UserCredential.query.filter_by(
                Email=payload['Email']).first()
            print(userCredential.Email)
            if userCredential:
                user = User.query.filter_by(
                    UserCredential=userCredential.UserCredentialId).first()
            else:
        
                return {"message": "admin not found"}, 404

            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            print(role.RoleName)
            if userCredential and payload['Password'] == userCredential.Password:
                roleStr = str(role.RoleName).split('.')[-1]
                response = flask.make_response()
                response.status_code = 200
                # response.headers["token"] = setToken(user.UserId, roleStr)
                
                tokenValue = setToken(user.UserId, roleStr)
                print(f"**************token : {tokenValue }")
                response.set_cookie("token",value = tokenValue,expires=10000000000,httponly=True)
                
                return response
            
        return {"message": "Incorrect email or password"}, 400
    
    @role_required('Admin')
    def get(self):
        return {"message": "you are logged in"}, 200

# if we want to log out the user we call the unsetToken() function
# example
@auth_admin.route("/logout")
class UserLogOut(Resource):
    def get(self):
        response = flask.make_response(jsonify({"message":"you are logged out"}))
        response.set_cookie("token",value="",expires=0,httponly=True)
        response.status_code = 200
        return response

@auth_admin.route('/register')
class UserRegisterResource(Resource):
    @auth_admin.expect(user)
    def post(self):
        payload = api.payload
        newRegisteredUser = payload
        newUser = User(
            FirstName=newRegisteredUser["FirstName"],
            LastName=newRegisteredUser["LastName"],
            UserName=newRegisteredUser["UserName"],
            BirthDate=newRegisteredUser["BirthDate"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            Gender=newRegisteredUser["Gender"],
            MartialStatus=newRegisteredUser["MaritalStatus"],
        )
        userRole = UserRole.query.filter_by(RoleName="Admin").first()
        userRole.Users.append(newUser)

        newUserCredential = payload
        newCredential = UserCredential(
            Email=newUserCredential["Email"],
            Password=newUserCredential["Password"]
        )
        newCredential.User = newUser
        print(newUserCredential)

        # newUserRole = UserRole

        db.session.add(newCredential)
        db.session.commit()

        print(newUser)
        db.session.add(newUser)
        db.session.commit()
        return userSchema.dump(newUser)
