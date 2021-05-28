from flask_restplus import Resource, Namespace
from eshiBlood.models.models import UserCredential, User
from eshiBlood import bcrypt, db
from eshiBlood.routes.routes import api
from eshiBlood.schema.ma import userCredential, user, userSchema
from datetime import datetime
from flask_jwt import jwt_required

auth_ns = Namespace('auth')

@auth_ns.route('/login')
class UserLoginResource(Resource):
    @auth_ns.expect(userCredential)
    def post(self):
        data = api.payload
        
        if data['Email'] != "" and data['Password'] != "":
            userCredential = UserCredential.query.filter_by(
                Email=data['Email']).first()
            
            if userCredential and data['Password'] == userCredential.Password:
                return {"message": "Logged in successfully"}, 200
            else:
                return {"message": "Email or password incorrect"}, 400

        return {"message": "user not found"}, 400    


    @jwt_required()    
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
        
        newCredentialUser = payload
        newCredential = UserCredential(
            Email=newCredentialUser["Email"],
            Password=newCredentialUser["Password"]
        )
        print(newCredentialUser)
        db.session.add(newCredential)
        db.session.commit()

        print(newUser)
        db.session.add(newUser)
        db.session.commit()
        return userSchema.dump(newUser)

