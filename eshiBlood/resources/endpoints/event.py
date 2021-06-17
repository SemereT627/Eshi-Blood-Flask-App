import flask
from flask import json
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime
from eshiBlood.schema.ma import eventSchema, addressSchema
from eshiBlood.utils.role_jwt import *
from sqlalchemy.orm import joinedload, query
from flask.json import jsonify

event_ns = Namespace("events")

@event_ns.route("")
@event_ns.route("/")
class EventResource(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def get(self):
        events = Event.query.filter_by(IsDeleted=0).all()
        
        # return eventSchema.dump(events)
        # return jsonify(event =Event.query.filter_by(IsDeleted=0).all())
        responseList = []
        for event in events:
            res = {}
            res["Status"] = event.Status.value
            res["EventName"] = event.EventName
            res["EventGoal"] = event.EventGoal
            res["TotalDonations"] = event.TotalDonations
            try:
                res["CreatedAt"] = event.CreatedAt.strftime("%m/%d/%Y, %H:%M:%S")
                res["UpdatedAt"] = event.UpdatedAt.strftime("%m/%d/%Y, %H:%M:%S")
                res["StartDate"] = event.StartDate.strftime("%m/%d/%Y, %H:%M:%S")
                res["EndDate"]=event.EndDate.strftime("%m/%d/%Y, %H:%M:%S")
            except:
                continue
            res["EventId"] = event.EventId
            res["EventSlogan"] = event.EventSlogan
            queriedOrganizer = User.query.filter_by(UserId = event.EventOrganizer).first()
            res["FirstName"] = queriedOrganizer.FirstName
            res["LastName"] = queriedOrganizer.LastName

            responseList.append(res)
        
        print(responseList)
        return responseList
        

    
    @role_required("Admin")
    def post(self):
        db.session.rollback()
        role = tokenRole()
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedUser = User.query.filter_by(UserId = uid).first()
        newEvent = Event()
        newEvent.EventGoal = int(payload["EventGoal"])
        newEvent.EventName = payload["EventName"]
        queriedUser.Events.append(newEvent)#event organizer
        newEvent.CreatedAt = datetime.datetime.now()
        newEvent.UpdatedAt = datetime.datetime.now()
        newEvent.EndDate = payload["EndDate"]
        newEvent.StartDate = payload["StartDate"]
        newEvent.EventSlogan = payload["EventSlogan"]
        newEvent.TotalDonations = 0

        newEvent.EventOrganizer = uid
        
        
        # TODO state,city,zone.....
        # address = Address()
        # address.State = payload["State"]
        # address.Event = newEvent


        db.session.add_all([newEvent])
        db.session.commit()
        return {"msg":"event created"}

@event_ns.route("/<int:id>")
class EventResourceId(Resource):
    @either_roles_required("Admin", "SuperAdmin", "Donor", "Nurse")
    def get(self,id):
        queriedEvent = Event.query.filter_by(EventId=id).first()
        return eventSchema.dump(queriedEvent,many=False)
    
    @role_required("Admin")
    def put(self,id):
        payload = api.payload
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedEvent = Event.query.filter_by(EventId=id).first()
        if(str(uid) == str(queriedEvent.EventOrganizer) ):
            queriedEvent.EventGoal = payload["EventGoal"]
            queriedEvent.EventName = payload["EventName"]
            queriedEvent.UpdatedAt = datetime.datetime.now()
            queriedAddress = Address.query.filter_by(AddressId = queriedEvent.Address).first()
            queriedAddress.State = payload["Address"]
            db.session.commit()
            return {"msg":"event updated"}
        else:
            return {"msg": "not yours to edit "},401

    @role_required("Admin")
    def delete(self,id):
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        queriedEvent = Event.query.filter_by(EventId=id).first()
        if(str(uid) == str(queriedEvent.EventOrganizer) ):
            queriedEvent.IsDeleted = 1
            db.session.commit()
            return {"msg":"event deleted"}
        else:
            return {"msg": "not yours to delete "},401


@event_ns.route("/<int:id>/appointments/")
class EventAppointmentsResource(Resource):
    @role_required("Donor")
    def post(self,id):
        db.session.rollback()
        payload = api.payload
        queriedEvent = Event.query.filter_by(EventId=id).first()
        token = request.headers.get("token")
        uid = getTokenUserId(token)
        # if(userCanBookAppointment()==True):
        if(queriedEvent!=None):
        
            newAppointment = Appointment()
            newAppointment.AppointmentDescription = payload["AppointmentDescription"]
            newAppointment.Discriminator = "Event"
            newAppointment.DiscriminatorId = queriedEvent.EventId
            newAppointment.CreatedAt = datetime.datetime.now()
            newAppointment.UpdatedAt = datetime.datetime.now()
            newAppointment.User = int(uid)
            db.session.add(newAppointment)
            db.session.commit()
            return {"msg":"event accepted"}
        else:
            return {"msg":"resource not found"}