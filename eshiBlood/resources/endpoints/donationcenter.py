import flask
from flask_restplus import Resource, Namespace
from werkzeug.datastructures import Accept
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
import datetime
from eshiBlood.schema.ma import donationCenterSchema,appointmentSchema
from eshiBlood.utils.role_jwt import *
from eshiBlood.resources.endpoints.operations import userCanBookAppointment

donationCenter_ns = Namespace("donationcenters")


@donationCenter_ns.route("/")
class DonationCenterResource(Resource):
    @either_roles_required("Admin","SuperAdmin","Donor")
    def get(self):
        dcs  = DonationCenter.query.filter_by(IsDeleted=0).all()
        dclist = []
        for dc in dcs:
            queriedAddress = Address.query.filter_by(AddressId=dc.Address).first()
            res = {}
            res["DonationCenterId"] = dc.DonationCenterId
            res["DonationCenterName"] = dc.DonationCenterName
            res["CreatedAt"] = dc.CreatedAt
            res["StartDate"] = "2021-06-17"
            res["EndDate"] = "2021-06-30"
            res["State"] = queriedAddress.State.value
            res["City"] = queriedAddress.City
            res["Status"] = dc.Status.value

            dclist.append(res)

        #return make_response({"donationcenters":dclist})
        return jsonify(dclist)
        #return donationCenterSchema.dump(dcs)
    # @role_required("Nurse")
    @role_required("Admin")
    def post(self):
        db.session.rollback()
        payload = api.payload
        token = flask.request.headers.get("token")
        uid = getTokenUserId(token)
        nurse = User.query.filter_by(UserId=uid).first()
        newDC = DonationCenter()
        
        newDC.DonationCenterName = payload["DonationCenterName"]
        newDC.CreatedAt = datetime.datetime.now()
        newDC.UpdatedAt = datetime.datetime.now()

        address = Address()
        address.State = payload["State"]
        address.Zone = payload["Zone"]
        address.City = payload["City"]
        address.Woreda = payload["Woreda"]
        #address.PhoneNumber = payload["PhoneNumber"]
        
        address.DonationCenter = newDC

        nurse.DonationCenters.append(newDC)

        db.session.add_all([newDC,address])
        db.session.commit()
        return "donation center created"

@donationCenter_ns.route("/<int:id>")
class DonationCentersResource(Resource):
    @either_roles_required("Admin","SuperAdmin","Donor","Nurse")
    def get(self,id):
        dcs = DonationCenter.query.filter_by(DonationCenterId=id).first()
        return donationCenterSchema.dump([dcs])
    # @role_required("Nurse")
    @role_required("Admin")
    def put(self,id):
        db.session.rollback()
        try:
            payload = api.payload
            queriedDC = DonationCenter.query.filter_by(DonationCenterId=id).first()
            if(queriedDC!=None):
                try:
                    queriedDC.DonationCenterName = payload["DonationCenterName"]
                    queriedDC.UpdatedAt = datetime.datetime.now()

                    queriedAddress = Address.query.filter_by(AddressId = queriedDC.Address).first()
                    if(queriedAddress==None):
                        db.session.commit()
                        return {"msg":"successfully updated"}
                    else:
                        print("((((((((((((((((((( non none")
                    queriedAddress.State = payload["State"]
                    queriedAddress.City = payload["City"]
                    queriedAddress.Zone = payload["Zone"]
                    queriedAddress.Woreda = payload["Woreda"]
                    # queriedAddress.AddressLine = payload["AddressLine"]
                    queriedAddress.PhoneNumber = payload["PhoneNumber"]
                    db.session.commit()
                    return {"msg":"successfully updated"}
                except:
                    return {"msg":"invalid input"}
            else:
                return {"msg":"Donation center doesn't exist"}

        except:
            return  {"msg":"Server error"}
    # @role_required("Nurse")
    @role_required("Admin")
    def delete(self,id):
        db.session.rollback()
        queriedDC = DonationCenter.query.filter_by(DonationCenterId = id).first()
        queriedDC.IsDeleted = 1
        db.session.commit()
        return {"msg":"Successfully updated"}
    

@donationCenter_ns.route("/<int:id>/<action>")
class NurseAppointmentResource(Resource):
    @role_required("Admin")
    def patch(self,id,action):
        queriedDonationCenter = DonationCenter.query.filter_by(DonationCenterId=id).first()
        if(queriedDonationCenter!=None):
            if(action=="accept"):
                queriedDonationCenter.Status = "Active"
            elif(action=="refuse" or action=="reject"):
                queriedDonationCenter.Status = "Closed"
            db.session.commit()
            return {"msg":f"donation center {action}ed"}
        else:
            return {"msg":"resource not found"}

@donationCenter_ns.route("/<int:id>/appointments")
class AppointmentThroughDonationCenter(Resource):
    @role_required("Donor")
    def post(self,id):
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        payload = api.payload
        # if(userCanBookAppointment()==True):
        queriedDC = DonationCenter.query.filter((DonationCenter.DonationCenterId==id)&(DonationCenter.Status=="Active")).first()
        
        if(queriedDC!=None):
            newAppointment = Appointment(
                AppointmentDescription=payload["AppointmentDescription"],
                CreatedAt=datetime.datetime.utcnow(),
                UpdatedAt=datetime.datetime.utcnow()
            )
            
            queriedDC.Appointments.append(newAppointment)
            queriedUser.Appointments.append(newAppointment)
            db.session.add(newAppointment)
            db.session.commit()
            # print(userCanBookAppointment())
            return {"message": "appointment created"}, 200
        else:
            return {"msg":"donation center not found"}
        # else:
        #     return {"msg":"wait three months to donate"}

@donationCenter_ns.route("/<int:id>/<action>")
class AdminDonationCenterAuthorize(Resource):
    @role_required("Admin")
    def patch(self,id,action):
        queriedDC = DonationCenter.query.filter_by(DonationCenterId=id).first()
        if(queriedDC==None):
            return {"msg":"Resource not found"}
        else:
            if(action=="Accept" or action=="accept"):
                queriedDC.Status = "Active"
                db.session.commit()
                return {"msg":"Donation Center Accepted"}
            elif(action=="Reject"):
                queriedDC.Status = "Closed"
                return {"msg":"Donation Center Rejected"}
    @role_required("Donor")
    def get(self,id,action):
        # queriedDC = DonationCenter.query.filter_by(DonationCenterId=id).first()
        queriedAppts = Appointment.query.filter((Appointment.DonationCenter==id)).all()#&(Appointment.Status=="Active")
        return appointmentSchema.dump(queriedAppts)
        
            


    


