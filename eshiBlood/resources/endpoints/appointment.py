import flask
from flask import json
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import appointmentSchema, appointment
from eshiBlood.utils.role_jwt import *

appointment_ns = Namespace("appointments")

# @appointment_ns.route("")
@appointment_ns.route("/")
class AppointmentResource(Resource):
    @either_roles_required("Admin","SuperAdmin","Nurse","Donor")
    def get(self):
        
        role = tokenRole()
        token = request.headers.get("token")

        if(role=="Admin" or role=="SuperAdmin"):
            appts = Appointment.query.filter_by(IsDeleted=0).all()
            apptList = []
            for appt in appts:
                res = {}
                queriedUser = User.query.filter_by(UserId=appt.User).first()
                res["AppointmentDescription"]=appt.AppointmentDescription
                res["CreatedAt"] = appt.CreatedAt
                res["AppointmentId"] = appt.AppointmentId
                res["Status"] = appt.Status.value
                res["DonationCenter"] = appt.DonationCenter
                res["Type"]=appt.Discriminator
                    
                res["UserName"] = queriedUser.FirstName + queriedUser.LastName
                apptList.append(res)
            
            return jsonify(apptList)
        
        elif(role=="Nurse"):
            user_id = getTokenUserId(token)
            nurse = User.query.filter_by(UserId=user_id).first()
            nurse_id = nurse.UserId
            appts = Appointment.query.filter_by(DonationCenter=nurse_id)
            nonDeletedAppts = [appt for appt in appts if str(appt.IsDeleted)=="0" ]
            return appointmentSchema.dump(nonDeletedAppts)
        elif(role=="Donor"):
            user_id = getTokenUserId(token)
            appts = Appointment.query.filter_by(User = user_id)
            nonDeletedAppts = [appt for appt in appts if str(appt.IsDeleted)=="0" ]
            return appointmentSchema.dump(nonDeletedAppts)
        else:
            return "unauthorized"
    # @role_required("Donor")
    # def post(self):
    #     token = request.headers.get("token")
    #     uid = getTokenUserId(token)
    #     queriedUser = User.query.filter_by(UserId = uid).first()
    #     payload = api.payload
    #     newAppointment = Appointment(
    #         AppointmentDescription=payload["AppointmentDescription"],
    #         CreatedAt=datetime.datetime.utcnow(),
    #         UpdatedAt=datetime.datetime.utcnow()
    #     )
    #     try:
    #         if(payload["Discriminator"]!=None):
    #             newAppointment.Discriminator  = payload["Discriminator"]
    #             newAppointment.DiscriminatorId = int(payload["DiscriminatorId"])
    #     except:
    #         pass
    #     queriedUser.Appointments.append(newAppointment)
    #     db.session.add(newAppointment)
    #     db.session.commit()
    #     return {"message": "appointment created"}, 200
@appointment_ns.route("/<int:id>")
class AppointmentsResource(Resource):
    @either_roles_required("Admin","SuperAdmin","Nurse","Donor")
    def get(self,id):
        
        role = tokenRole()
        token = request.headers.get("token")
        if(role=="Admin" or role=="SuperAdmin"):
            data = Appointment.query.filter_by(AppointmentId = id).first()
            return appointmentSchema.dump([data])
        elif(role=="Nurse"):
            uid = getTokenUserId(token)
            
            donationCenters = DonationCenter.query.filter_by(UpdatedBy=uid).all()
            apptsList = []
            for dc in donationCenters:
                dc_id = dc.DonationCenterId
                appts = DonationCenter.query.filter_by(UpdatedBy=dc_id).all()
                print(dc.DonationCenterName)
                for appt in appts:
                    apptsList.append(appt)
            appts = [appt for appt in apptsList if appt.IsDeleted==0]
            return appointmentSchema.dump(appts)
        elif(role=="Donor"):
            uid = getTokenUserId(token)
            queriedAppointments = Appointment.query.filter_by(User=uid)
            queriedAppointment = [qAppt for qAppt in queriedAppointments if qAppt.AppointmentId==id]
            
            if(len(queriedAppointment)!=0):
                qAppt = queriedAppointment[0]
                # data = Appointment.query.filter_by(AppointmentId=id).first()
                print(qAppt.AppointmentId)
                return appointmentSchema.dump([qAppt])
            else:
                return "appointment not authorized to be accessed"
    

    @role_required("Donor")
    def put(self, id):
        '''
        Updates an appointment
        '''
        # result = Appointment.query.filter_by(AppointmentId=id).first()
        payload = api.payload
        
        token = flask.request.headers.get("token")
        uid = getTokenUserId(token)
        queriedAppointments = Appointment.query.filter_by(User=uid)
        queriedAppointment = [appt for appt in queriedAppointments if appt.AppointmentId==id]
        if(len(queriedAppointment)!=0):
            qAppt = queriedAppointment[0]
            # qAppt.StartDate = payload["StartDate"]
            # qAppt.EndDate = payload["EndDate"]
            # qAppt.StartTime = payload["StartTime"]
            # qAppt.EndTime = payload["EndTime"]
            # print("////////////////////////////////////////////////////////////////")
            
            qAppt.Status = payload["Status"]
            qAppt.AppointmentDescription = payload["AppointmentDescription"]
            qAppt.UpdatedAt = datetime.datetime.utcnow()
            db.session.commit()
            return appointmentSchema.dump([qAppt]), 204    
        else:
            return "not yours appointment to update"
    @role_required("Donor")
    def delete(self,id):
        '''
        Deletes an appointment
        '''
        # result = Appointment.query.filter_by(AppointmentId=id).first()
        token = flask.request.headers.get("token")
        uid = getTokenUserId(token)
        queriedAppointments = Appointment.query.filter_by(User=uid)
        queriedAppointment = [i for i in queriedAppointments if i.AppointmentId==id]
        if(len(queriedAppointment)!=0):
            qAppt = queriedAppointment[0]
        
            qAppt.IsDeleted = 1
            # print(qAppt.AppointmentDescription)
            db.session.commit()
            return {"message":"deleted successfully"}, 200
        else:
            return "not your appointment to delete"


@appointment_ns.route("/<int:id>/<action>/")
class AdminAppointmentResource(Resource):
    # @role_required("Nurse")
    @role_required("Admin")
    def get(self,id,action):
        print("===================================================================================")
        queriedAppointment = Appointment.query.filter_by(AppointmentId=id).first()
    
        if(queriedAppointment!=None):
            if(action=="accept" and queriedAppointment.Status.value != "Active"):
                
                queriedAppointment.Status = "Active"
                if(queriedAppointment.Discriminator!=None and queriedAppointment.Discriminator!=""):
                    if(queriedAppointment.DiscriminatorId!=None and queriedAppointment.DiscriminatorId!=""):
                        # TODO increment event's or request's total donations
                        if(queriedAppointment.Discriminator=="Event"):
                            queriedEvent = Event.query.filter_by(EventId=queriedAppointment.DiscriminatorId).first()
                            if(queriedEvent.TotalDonations == None or queriedEvent.TotalDonations == ""):
                                queriedEvent.TotalDonations = 1
                            else:
                                queriedEvent.TotalDonations = queriedEvent.TotalDonations + 1
                        elif(queriedAppointment.Discriminator=="Request"):
                            queriedRequest = Request.query.filter_by(RequestId=queriedAppointment.DiscriminatorId).first()
                            if(queriedRequest.TotalDonation == None or queriedRequest.TotalDonation == ""):
                                queriedRequest.TotalDonation = 1
                            else:
                                queriedRequest.TotalDonation = queriedRequest.TotalDonation + 1
                                
            elif(action=="refuse" or action=="reject"):
                queriedAppointment.Status = "Closed"
            db.session.commit()
            return {"msg":f"appointment {action}ed"}
        else:
            return {"msg":"resource not found"}
        
        

