from flask_restplus import Resource, Namespace
from eshiBlood.models.models import Event
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import eventSchema, event
from eshiBlood.utils.role_jwt import role_required, getTokenUserId

event_admin_ns = Namespace('admin/events')


@event_admin_ns.route('/<int:id>')
class EventResource(Resource):
    @role_required('SuperAdmin')
    @event_admin_ns.expect(event)
    def get(self, id):
        '''
        Show single event
        '''
        data = Event.query.filter_by(EventId=id).first()
        print(data)
        return eventSchema.dump([data])

    @role_required('SuperAdmin')
    @event_admin_ns.expect(event)
    def put(self, id):
        '''
        Updates an event
        '''
        updateEvent = Event.query.filter_by(EventId=id).first()
        payload = api.payload
        updateEvent.EventName=payload["EventName"]
        updateEvent.EventGoal=payload["EventGoal"]
        updateEvent.TotalDonations=payload["TotalDonations"]
        updateEvent.Status=payload["Status"]
        updateEvent.UpdatedAt=datetime.utcnow()
        db.session.commit()
        return {"message": "OK"}, 204 #It updates check with status code 200

    @role_required('SuperAdmin')
    def delete(self,id):
        '''
        Deletes an event
        '''
        result = Event.query.filter_by(EventId=id).first()
        result.IsDeleted = 1
        db.session.commit()
        return {"message":"deleted successfully"}

@event_admin_ns.route('')
class EventsResource(Resource):
    @role_required('SuperAdmin')
    def get(self):
        '''
        Show all events
        '''
        data = Event.query.filter_by(IsDeleted=0).all()
        return eventSchema.dump(data)

    @role_required('SuperAdmin')
    @event_admin_ns.expect(event)
    def post(self):
        '''
        Creates an event
        '''
        payload = api.payload
        newEvent = Event(
            EventName=payload["EventName"],
            EventGoal=payload["EventGoal"],
            TotalDonations=payload["TotalDonations"],
            Status=payload["Status"],
            CreatedAt=datetime.utcnow(),
            UpdatedAt=datetime.utcnow(),
            IsDeleted=0
        )
        db.session.add(newEvent)
        db.session.commit()
        return {"message": "Event created successfully"}, 200
