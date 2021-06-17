import flask
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import requestSchema, addressSchema
from eshiBlood.utils.role_jwt import *
from eshiBlood.resources.endpoints.operations import userCanBookAppointment

request_ns = Namespace("requests")


@request_ns.route("")
@request_ns.route("/")
class RequestResources(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def get(self):

        role = tokenRole()
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        # if(role=="Donor"):#not needed
        #     queriedRequests = Request.query.filter_by(CreatedBy=uid).all()
        #     nonDeletedRequests = [req for req in queriedRequests if req.IsDeleted==1]
        #     return requestSchema.dump(nonDeletedRequests)
        # else:
        queriedRequests = Request.query.filter_by(IsDeleted=0).all()
        return requestSchema.dump(queriedRequests)

    @role_required("Admin")
    def post(self):
        db.session.rollback()
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId=uid).first()
        newRequest = Request()
        newRequest.UnitsNeeded = int(payload["UnitsNeeded"])
        newRequest.RequestReason = payload["RequestReason"]
        newRequest.CreatedBy = uid
        newRequest.CreatedAt = datetime.datetime.now()
        newRequest.UpdatedAt = datetime.datetime.now()
        newRequest.TotalDonation = 0
        # newRequest.BloodTypes

        bt = BloodType.query.filter_by(
            BloodTypeName=payload["BloodType"]).first()
        bt.Requests.append(newRequest)


        # newRequest.Address
        address = Address()
        # address.State = payload["State"]
        # address.Zone = payload["Zone"]
        # address.City = payload["City"]
        # address.Woreda = payload["Woreda"]
        # address.PhoneNumber = payload["PhoneNumber"]

        address.Request = newRequest

        db.session.add_all([newRequest, address])
        db.session.commit()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
        # print(type(bloodTypeSchema))

        # return {"Request": requestSchema.dump(newRequest, many=False), "BloodType": payload["BloodType"], "Address": addressSchema.dump(address, many=False)}
        return requestSchema.dump(newRequest,many=False)


@request_ns.route("/<int:id>")
class RequestResourcesId(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def get(self, id):
        role = tokenRole()
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedRequests = Request.query.filter(
            (Request.IsDeleted == 0) & (Request.RequestId == id)).first()
        return requestSchema.dump([queriedRequests])

    @role_required("Admin")
    def put(self, id):
        db.session.rollback()
        payload = api.payload

        queriedRequest = Request.query.filter_by(RequestId=id).first()
        queriedRequest.UnitsNeeded = int(payload["UnitsNeeded"])
        queriedRequest.RequestReason = payload["RequestReason"]
        queriedRequest.UnitsNeeded = int(payload["UnitsNeeded"])
        queriedRequest.RequestReason = payload["RequestReason"]
        queriedRequest.UpdatedAt = datetime.datetime.now()
        bt = BloodType.query.filter_by(
            BloodTypeName=payload["BloodType"]).first()
        bt.Requests.append(queriedRequest)

        # queriedRequest.Address
        address = Address.query.filter_by(
            AddressId=queriedRequest.Address).first()
        address.State = payload["State"]
        address.Zone = payload["Zone"]
        address.City = payload["City"]
        address.Woreda = payload["Woreda"]
        address.PhoneNumber = payload["PhoneNumber"]

        db.session.commit()
        return {"msg": "request updated"}

    @role_required("Admin")
    def delete(self, id):
        db.session.rollback()
        queriedRequest = Request.query.filter_by(RequestId=id).first()
        queriedRequest.IsDeleted = 1
        db.session.commit()
        return {"msg": "request deleted"}


@request_ns.route("/<int:id>/appointments/")
class DonorRequestAppointment(Resource):
    @role_required("Donor")
    def post(self, id):
        db.session.rollback()
        payload = api.payload
        queriedRequest = Request.query.filter_by(RequestId=id).first()
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        # if(userCanBookAppointment()==True):
        if(queriedRequest!=None):
            
            # queriedRequest.Status = "Active"
            # check if the donor is eligible to donate
            newAppointment = Appointment()
            newAppointment.AppointmentDescription = payload["AppointmentDescription"]
            newAppointment.Discriminator = "Request"
            newAppointment.DiscriminatorId = queriedRequest.RequestId
            newAppointment.CreatedAt = datetime.datetime.now()
            newAppointment.UpdatedAt = datetime.datetime.now()
            newAppointment.User = int(uid)
            db.session.add(newAppointment)
            db.session.commit()
            return {"msg":"request accepted"}
        else:
            return {"msg":"resource not found"}
        # else:
        #     return {"msg":"wait three months to donate"}

