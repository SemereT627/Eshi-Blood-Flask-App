from flask_restplus import Resource, reqparse, fields
from eshiBlood.models.models import UserCredential
from eshiBlood import bcrypt, db, api
from eshiBlood.schema.ma import *


userCredentialSchema = UserCredentialSchema()
userCredential = api.model("UserCredential", {
    'Email': fields.String('Your Email'),
    'Password':fields.String('Password')
})

userSchema = UserSchema()
user = api.model("User",{
    "FirstName":fields.String,
    "LastName":fields.String,
    "UserName":fields.String,
    "BirthDate":fields.Date,
    "MaritalStatus":fields.Boolean,
    "BloodType":fields.String,
    "Address":fields.String
})


class UserLogin(Resource):
    @api.expect(userCredential)
    def post(self):
        data = api.payload
    
        if data['email'] == None and data['password'] == None:
            return {"message":"fields cannot be empty"}
        
        userCredential = UserCredential.query.filter_by(
            Email=data['email']).first()

        if userCredential:
            return {"message": "A user with that email exists."}, 400

        user = UserCredential(Email=data['email'], Password=data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201


class UserRegister(Resource):
    @api.expect(user)
    def post(self):
        newUser = User()
        newUserFromRequest = api.payload
        newUser.FirstName = newUserFromRequest["FirstName"]
        newUser.LastName = newUserFromRequest["LastName"]
        newUser.UserName = newUserFromRequest["UserName"]
        newUser.BirthDate = newUserFromRequest["BirthDate"]
        newUser.MartialStatus = newUserFromRequest["MaritalStatus"]
        newUser.BloodType = newUserFromRequest["BloodType"]
        newUser.Address = newUserFromRequest["Address"]
        print(newUser)
        db.session.add(newUser)
        db.session.commit()
        return userSchema.dump(newUser)

