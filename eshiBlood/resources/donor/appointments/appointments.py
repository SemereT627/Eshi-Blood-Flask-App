from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Appointment
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import appointmentSchema, appointment
from eshiBlood.utils.role_jwt import *
import flask

appointment_donor_ns = Namespace('donor/appointments')


@appointment_donor_ns.route('/<int:id>')
class AppointmentResource(Resource):
    @appointment_donor_ns.expect(appointment)
    @role_required("Donor")
    def get(self, id):
        '''
        Show single appointment
        '''
        token = flask.request.cookies.get("token")
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

    @appointment_donor_ns.expect(appointment)
    @role_required("Donor")
    def put(self, id):
        '''
        Updates an appointment
        '''
        # result = Appointment.query.filter_by(AppointmentId=id).first()
        payload = api.payload
        
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        queriedAppointments = Appointment.query.filter_by(User=uid)
        queriedAppointment = [appt for appt in queriedAppointments if appt.AppointmentId==id]
        if(len(queriedAppointment)!=0):
            qAppt = queriedAppointment[0]
            qAppt.StartDate = payload["StartDate"]
            qAppt.EndDate = payload["EndDate"]
            qAppt.StartTime = payload["StartTime"]
            qAppt.EndTime = payload["EndTime"]
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
        token = flask.request.cookies.get("token")
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


@appointment_donor_ns.route('')
class AppointmentsResource(Resource):
    @appointment_donor_ns.expect(appointment)
    @role_required("Donor")
    def post(self):
        '''
        Creates an appointment
        '''
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        payload = api.payload
        newAppointment = Appointment(
            # StartDate=payload["StartDate"],
            # EndDate=payload["EndDate"],
            # StartTime=payload["StartTime"],
            # EndTime=payload["EndTime"],
            # Status=payload["Status"],
            AppointmentDescription=payload["AppointmentDescription"],
            CreatedAt=datetime.datetime.utcnow(),
            UpdatedAt=datetime.datetime.utcnow(),
            IsDeleted=0
        )
        queriedUser.Appointments.append(newAppointment)
        db.session.add(newAppointment)
        db.session.commit()
        return {"message": "appointment created"}, 200
    @role_required("Donor")
    def get(self):
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        qAppt = Appointment.query.filter_by(User=uid)
        queriedAppointment = [i for i in qAppt if  str( i.IsDeleted)=="0"]
        return appointmentSchema.dump(queriedAppointment)

    
