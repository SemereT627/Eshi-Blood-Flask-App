from flask_restplus import Resource, Namespace
from eshiBlood.models.models import UserCredential, User, UserRole
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
# from flask_jwt import jwt_required
from eshiBlood.utils.role_jwt import role_required, getTokenUserId, setToken

auth_ns = Namespace('auth')

@auth_ns.route('/login')
class UserLoginResource(Resource):
    
    @auth_ns.expect(userCredential)
    def post(self):
        data = api.payload
        
        if data['Email'] != "" and data['Password'] != "":
            userCredential = UserCredential.query.filter_by(
                Email=data['Email']).first()
            user = User.query.filter_by(
                UserCredential=userCredential.UserCredentialId
            ).first()

            role = UserRole.query.filter_by(UserRoleId=user.UserRole).first()
            if userCredential and data['Password'] == userCredential.Password:
                roleStr = str(role.RoleName).split('.')[-1]
                # tok = str(setToken(user.UserId,roleStr),'utf-8')
                # print(setToken(user.UserId,roleStr))
                # return {"x":"y"}
                return setToken(user.UserId,roleStr), 200
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "user not found"}, 400    

    @role_required('Donor')
    def get(self):
        return {"Message":"You are Logged In"}

@auth_ns.route('/register')
class UserRegisterResource(Resource):
    @auth_ns.expect(user)
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

