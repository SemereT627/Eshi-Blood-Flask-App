from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Appointment
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import appointmentSchema, appointment

appointment_ns = Namespace('appointments')


@appointment_ns.route('/<int:id>')
class AppointmentResource(Resource):
    def get(self, id):
        '''
        Show single appointment
        '''
        data = Appointment.query.filter_by(AppointmentId=id).first()
        print(data.AppointmentId)
        return appointmentSchema.dump([data])

    @appointment_ns.expect(appointment)
    def put(self, id):
        '''
        Updates an appointment
        '''
        result = Appointment.query.filter_by(AppointmentId=id).first()

        return appointmentSchema.dump(result)


@appointment_ns.route('')
class AppointmentsResource(Resource):
    def get(self):
        '''
        Show all appointments
        '''
        data = Appointment.query.all()
        return appointmentSchema.dump(data)

    @appointment_ns.expect(appointment)
    def post(self):
        '''
        Creates an appointment
        '''
        payload = api.payload
        newAppointment = Appointment(
            StartDate=payload["StartDate"],
            EndDate=payload["EndDate"],
            StartTime=payload["StartTime"],
            EndTime=payload["EndTime"],
            Status=payload["Status"],
            AppointmentDescription=payload["AppointmentDescription"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow()
        )
        db.session.add(newAppointment)
        db.session.commit()
        return {"message": "appointment created"}, 200
