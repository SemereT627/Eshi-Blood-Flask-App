import flask
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Appointment
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import appointmentSchema, appointment
from eshiBlood.utils.role_jwt import *

appointment_admin_ns = Namespace('admin/appointments')


@appointment_admin_ns.route('/<int:id>')
class AppointmentResource(Resource):
    @role_required('SuperAdmin')
    @appointment_admin_ns.expect(appointment)
    def get(self, id):
        '''
        Show single appointment
        '''
        data = Appointment.query.filter_by(AppointmentId=id).first()
        print(data.AppointmentId)
        return appointmentSchema.dump([data])

    @role_required('SuperAdmin')
    @appointment_admin_ns.expect(appointment)
    def put(self, id):
        '''
        Updates an appointment
        '''
        result = Appointment.query.filter_by(AppointmentId=id).first()
        payload = api.payload

        result.StartDate = payload["StartDate"]
        result.EndDate = payload["EndDate"]
        result.StartTime = payload["StartTime"]
        result.EndTime = payload["EndTime"]
        result.Status = payload["Status"]
        result.AppointmentDescription = payload["AppointmentDescription"]
        result.UpdatedAt = datetime.utcnow()
        db.session.commit()

        return appointmentSchema.dump([result]), 204    

    @role_required('SuperAdmin')
    def delete(self,id):
        '''
        Deletes an appointment
        '''
        result = Appointment.query.filter_by(AppointmentId=id).first()
        result.IsDeleted = 1
        db.session.commit()
        return {"message":"deleted successfully"}, 200


@appointment_admin_ns.route('')
class AppointmentsResource(Resource):
    @role_required('SuperAdmin')
    def get(self):
        '''
        Show all appointments
        '''
        data = Appointment.query.filter_by(IsDeleted=0).all()
        return appointmentSchema.dump(data)

    @role_required('SuperAdmin')
    @appointment_admin_ns.expect(appointment)
    def post(self):
        '''
        Creates an appointment
        '''
        payload = api.payload
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        newAppointment = Appointment(
            # StartDate=payload["StartDate"],
            # EndDate=payload["EndDate"],
            # StartTime=payload["StartTime"],
            # EndTime=payload["EndTime"],
            # Status=payload["Status"],
            AppointmentDescription=payload["AppointmentDescription"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            IsDeleted=0
        )
        queriedUser.Appointments.append(newAppointment)
        db.session.add(newAppointment)
        db.session.commit()
        return {"message": "appointment created"}, 200
