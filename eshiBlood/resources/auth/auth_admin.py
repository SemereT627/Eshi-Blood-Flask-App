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
        
                return {"message": "admin not found"}

            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            print(role.RoleName)
            if userCredential and payload['Password'] == userCredential.Password:
                roleStr = str(role.RoleName).split('.')[-1]
        
                return setToken(user.UserId, roleStr), 200
            
        return {"message": "Incorrect email or password"}, 400
    
    @role_required('Admin')
    def get(self):
        return {"message": "you are logged in"}, 200


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
