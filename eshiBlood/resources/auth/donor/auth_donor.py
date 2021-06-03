from flask_restplus import Resource, Namespace
import flask
from eshiBlood.models.models import UserCredential, User, UserRole
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
# from flask_jwt import jwt_required
from eshiBlood.utils.role_jwt import role_required, getTokenUserId, setToken




donor_auth_ns = Namespace('auth-donor')
#************************************************** DONOR auth begin ******************************************************
@donor_auth_ns.route('/login')
class UserLoginResource(Resource):
    
    @donor_auth_ns.expect(userCredential)
    def post(self):
        data = api.payload
        print("**************** auth-donor-login")
        
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
                response = flask.make_response()
                response.status_code = 200
                tokenValue = setToken(user.UserId,roleStr)
                # response.set_cookie("token",value = tokenValue,expires=10000000000,httponly=True)
                print(tokenValue)
                print(f"{userCredential.Password} {data['Password'] == userCredential.Password}")
                response.set_cookie(key="token",value = tokenValue,expires=10000000000,httponly=True)
                return response
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "Email or password cannot be empty"}, 400    

    @role_required('Donor')
    def get(self):
        return {"Message":"You are Logged In"}


@donor_auth_ns.route('/register')
class UserRegisterResource(Resource):
    @donor_auth_ns.expect(user)
    def post(self):
        payload = api.payload
        newRegisteredUser = payload
        newUser = User(
            FirstName=newRegisteredUser["FirstName"], 
            LastName=newRegisteredUser["LastName"], 
            UserName=newRegisteredUser["UserName"], 
            BirthDate=newRegisteredUser["BirthDate"],
            # is deleted
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            Gender=newRegisteredUser["Gender"],
            MartialStatus=newRegisteredUser["MaritalStatus"], 
            )
        userRole = UserRole.query.filter_by(RoleName="Donor").first()
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

#************************************************** DONOR auth end ******************************************************