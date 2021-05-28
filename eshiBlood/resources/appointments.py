from flask_restplus import Resource
from eshiBlood.models.models import Appointment
from eshiBlood import db, api
from datetime import datetime
from eshiBlood.schema.ma import appointmentSchema, appointment


class AppointmentResource(Resource):
    def get(self):
        data = Appointment.query.all()
        print(data)
        return appointmentSchema.dump(data)

    @api.expect(appointment)
    def post(self):
        payload = api.payload
        appointment = Appointment(StartDate=payload["StartDate"],EndDate=payload["EndDate"],StartTime=payload["StartTime"],EndTime=payload["EndTime"],Status=payload["Status"],AppointmentDescription=payload["AppointmentDescription"])
        db.session.add(appointment)
        db.session.commit()
        return {"message": "added appointment to database"}, 200
