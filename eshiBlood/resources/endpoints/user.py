import flask
from flask_restplus import Resource, Namespace, namespace
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import userSchema
from eshiBlood.utils.role_jwt import *
from eshiBlood.resources.endpoints.operations import userCanBookAppointment


user_ns = Namespace("/user")



@user_ns.route("/details/")
class userDetailResources(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def get(self):
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId=uid).first()
        # queriedUser = User()#test
        res = {}
        res["UserId"]=queriedUser.UserId
        res["FirstName"]=queriedUser.FirstName
        res["LastName"]=queriedUser.LastName
        res["UserName"]=queriedUser.UserName
        res["Gender"]=queriedUser.Gender.value
        res["BirthDate"]=queriedUser.BirthDate.strftime("%m/%d/%Y")
        res["CreatedAt"]=queriedUser.CreatedAt.strftime("%m/%d/%Y")
        res["UpdatedAt"]=queriedUser.UpdatedAt.strftime("%m/%d/%Y")
        res["MartialStatus"]=queriedUser.MartialStatus.value
        print("           00000000000000000000000000000000")
        print(queriedUser)
        queriedBloodType = BloodType.query.filter_by(BloodTypeId=queriedUser.BloodType).first()
        res["BloodType"]=queriedBloodType.BloodTypeName
        # address
        queriedAddress = Address.query.filter_by(AddressId=queriedUser.Address).first()
        queriedCredential = UserCredential.query.filter_by(UserCredentialId=queriedUser.UserCredential).first()
        res["State"]= queriedAddress.State.value
        res["Zone"]= queriedAddress.Zone
        res["Woreda"]= queriedAddress.Woreda
        res["PhoneNumber"] = queriedAddress.PhoneNumber
        res["Email"] = queriedCredential.Email
        queriedAppts = Appointment.query.filter((Appointment.User==uid)&(Appointment.Status=="Active")).all()
        res["Appointments"] = len(queriedAppts)
        
        return res

@user_ns.route("/")
class userResource(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def put(self):
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        queriedUser.FirstName = payload["FirstName"]
        queriedUser.LastName = payload["LastName"]
        queriedUser.UserName = payload["UserName"]
        queriedUser.Gender = payload["Gender"]
        queriedUser.BirthDate = payload["BirthDate"]
        queriedUser.UpdatedAt = datetime.datetime.now()
        queriedUser.MartialStatus = payload["MartialStatus"]
        queriedBloodType = BloodType.query.filter_by(BloodTypeName=payload["BloodType"]).first()
        queriedBloodType.Users.append(queriedUser)
        
        queriedAddress = Address.query.filter_by(AddressId = queriedUser.Address).first()
        queriedAddress.State = payload["State"]
        queriedAddress.Zone = payload["Zone"]
        queriedAddress.Woreda = payload["Woreda"]
        queriedAddress.PhoneNumber = payload["PhoneNumber"]
        
        newCredential = UserCredential.query.filter_by(UserCredentialId=queriedUser.UserCredential).first()
        newCredential.Email = payload["Email"]
        newCredential.Password = payload["Password"]

        db.session.commit()
        return {"msg":"user updated"}
    # def post(self):
    #     payload = api.payload
    #     token = request.headers.get("token")
    #     uid = getTokenUserId(token)
    #     newUser = User()
    #     newUser.FirstName = payload["FirstName"]
    #     newUser.LastName = payload["LastName"]
    #     newUser.UserName = payload["UserName"]
    #     newUser.Gender = payload["Gender"]
    #     newUser.BirthDate = payload["BirthDate"]
    #     newUser.CreatedAt = datetime.datetime.now()
    #     newUser.UpdatedAt = datetime.datetime.now()
    #     newUser.MartialStatus = payload["MartialStatus"]
    #     queriedBloodType = BloodType.query.filter_by(BloodTypeName=payload["BloodType"]).first()
    #     queriedBloodType.Users.append(newUser)
        
    #     newAddress = Address()
    #     newAddress.State = payload["State"]
    #     newAddress.Zone = payload["Zone"]
    #     newAddress.Woreda = payload["Woreda"]
    #     newAddress.PhoneNumber = payload["PhoneNumber"]

    #     newAddress.User = newUser
        
    #     newCredential = UserCredential()
    #     newCredential.Email = payload["Email"]
    #     newCredential.Password = payload["Password"]

    #     newCredential.User = newUser

    #     queriedRole = UserRole.query.filter_by(RoleName="Donor").first()
    #     queriedRole.Users.append(newUser)

    #     db.session.add_all([newUser,newAddress,newCredential])
    #     db.session.commit()
    #     return {"msg":"user created"}
    



