from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Event,User,Appointment
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import eventSchema, event,appointment
import flask
from eshiBlood.utils.role_jwt import *

event_donor_ns = Namespace('donor/events')
# @event_donor_ns.route("/<int:eid>/appointments/<int:aid>")
@event_donor_ns.route("/<int:eid>/appointments")
class EventAppointmentResource(Resource):
    @event_donor_ns.expect(appointment)
    @role_required("Donor")
    def post(self,eid):
        '''
        Creates an appointment
        '''
        # try:
        print("*************************** here")
        
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        payload = api.payload
        newAppointment = Appointment(
            AppointmentDescription=payload["AppointmentDescription"],
            CreatedAt=datetime.datetime.utcnow(),
            UpdatedAt=datetime.datetime.utcnow()
        )
        

        queriedEvent = Event.query.filter_by(EventId=eid).first()
        newAppointment.Discriminator = "Event"
        newAppointment.DiscriminatorId = queriedEvent.EventId
        queriedUser.Appointments.append(newAppointment)
        db.session.rollback()
        db.session.add(newAppointment)
        db.session.commit()
        return {"message": "appointment created"}, 200
        # except:
        #     return {"message":"invalid input"},400

        



@event_donor_ns.route('/<int:id>')
class EventResource(Resource):
    @event_donor_ns.expect(event)
    def get(self, id):
        '''
        Show single event
        '''
        data = Event.query.filter_by(EventId=id).first()
        print(data)
        return eventSchema.dump([data])

    @event_donor_ns.expect(event)
    def put(self, id):
        '''
        Updates an event
        '''
        payload = api.payload
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        
        queriedUser = User.query.filter_by(UserId = uid).first()

        eventToBeUpdated = Event.query.filter_by(EventId=id).first()
        if(queriedUser.UserId == eventToBeUpdated.EventOrganizer):
            eventToBeUpdated.EventName=payload["EventName"]
            eventToBeUpdated.EventGoal=payload["EventGoal"]
            eventToBeUpdated.TotalDonations=payload["TotalDonations"]
            eventToBeUpdated.Status=payload["Status"]
            eventToBeUpdated.UpdatedAt=datetime.datetime.utcnow()
            db.session.commit()
            return {"message": "OK"}, 200 #It updates check with status code 200
        else:
            return {"message":"Un authorized access"},400

            

    def delete(self,id):
        '''
        Deletes an event
        '''
        try:
            token = flask.request.cookies.get("token")
            uid = getTokenUserId(token)
            
            queriedUser = User.query.filter_by(UserId = uid).first()
            result = Event.query.filter_by(EventId=id).first()
            if(queriedUser.UserId==result.EventOrganizer):
                result.IsDeleted = 1
                db.session.commit()
                return {"message":"deleted successfully"}
            else:
                return {"message":"unauthorized"},400
        except:
            return {"message":"such record doesnt exist"}

@event_donor_ns.route('')
class EventsResource(Resource):
    @event_donor_ns.expect(event)
    def post(self):
        '''
        Creates an event
        '''
        token = flask.request.cookies.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()

        payload = api.payload
        newEvent = Event(
            EventName=payload["EventName"],
            EventGoal=payload["EventGoal"],
            TotalDonations=payload["TotalDonations"],
            Status=payload["Status"],
            CreatedAt=datetime.datetime.utcnow(),
            UpdatedAt=datetime.datetime.utcnow()
        )
        queriedUser.Events.append(newEvent)
        db.session.rollback()
        db.session.add(newEvent)
        db.session.commit()
        return {"message": "Event created successfully"}, 200
    def get(self):
        '''
        gets all events 
        '''
        token = flask.request.cookies.get("token")
        uid=getTokenUserId(token)
        qEvents = Event.query.all()
        
        events =[e for e in qEvents if e.EventOrganizer==int(uid)]
        print(len(events))
        eventsNotDeleted =  [e for e in events if str(e.IsDeleted)=="0"]
        return eventSchema.dump(eventsNotDeleted)
