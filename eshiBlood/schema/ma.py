from operator import mod
from flask_restplus import fields
from flask_sqlalchemy import model
from eshiBlood.models.models import UserCredential, User
from flask_marshmallow import Marshmallow
from eshiBlood.models.models import *
from eshiBlood.routes.routes import api
from marshmallow_enum import EnumField

ma = Marshmallow()


class UserSchema(ma.Schema):
    MartialStatus = EnumField(MartialStatus, by_value=True)
    Gender = EnumField(Gender, by_value=True)
    class Meta:
        fields = ("FirstName", "LastName", "UserName", "BirthDate",
                  "Gender", "MartialStatus")
        model = User


class UserCredentialSchema(ma.Schema):
    class Meta:
        fields = ("Email", "Password")
        model = UserCredential


class AppointmentSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)

    class Meta:
        fields = ("AppointmentId", "StartDate", "EndDate", "StartTime", "EndTime",
                  "Status", "AppointmentDescription", "DonationCenter")
        model = Appointment


class EventSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)

    class Meta:
        fields = ("EventId","EventName", "EventGoal", "EventOrganizer",
                  "TotalDonations", "Status", "CreatedAt", "UpdatedAt", "StartDate","EndDate","EventSlogan")
        model = Event


class RequestSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)

    class Meta:
        fields = ("RequestId","RequestReason", "UnitsNeeded", "BloodType",
                  "TotalDonation", "Status", "CreatedAt", "UpdatedAt")
        model = Request


class AddressSchema(ma.Schema):
    class Meta:
        fields = ("State", "City", "Subcity", "Woreda",
                  "Kebele", "Zone", "AddressLine", "PhoneNumber")
        model = Address


class DonationCenterSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)

    class Meta:
        fields = ("DonationCenterName", "Status", "UpdatedBy", "CreatedAt", "UpdatedAt", "DonationCenterId")
        model = DonationCenter

# Timeslot


class BloodTypeSchema(ma.Schema):
    class Meta:
        fields = ("BloodTypeName", "BloodTypeDescription")
        model = BloodType


class EmergencyContactSchema(ma.Schema):
    class Meta:
        fields = ("ContactName", "ContactPhone", "BloodType")
        model = EmergencyContact

class DonationHistorySchema(ma.Schema):
    class Meta:
        fields = ("CreatedAt","AppointmentId")


userSchema = UserSchema()
user = api.model("User", {
    "FirstName": fields.String,
    "LastName": fields.String,
    "UserName": fields.String,
    "BirthDate": fields.DateTime,
    "Gender": fields.String,
    "MaritalStatus": fields.String
})


userCredentialSchema = UserCredentialSchema()
userCredential = api.model("UserCredential", {
    'Email': fields.String('Your Email'),
    'Password': fields.String('Password')
})


appointmentSchema = AppointmentSchema(many=True)
appointment = api.model("Appointment", {
    "AppointmentId": fields.Integer,
    "StartDate": fields.DateTime,
    "EndDate": fields.DateTime,
    "StartTime": fields.DateTime,
    "EndTime": fields.DateTime,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "AppointmentDescription": fields.String
})

eventSchema = EventSchema(many=True)
event = api.model("Event", {
    "EventId":fields.Integer,
    "EventName": fields.String,
    "EventGoal": fields.Integer,
    "EventSlogan": fields.String,
    "EventOrganizer": fields.Integer,
    "TotalDonations": fields.Integer,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "CreatedAt": fields.DateTime,
    "UpdatedAt": fields.DateTime,
    "StartDate":fields.DateTime,
    "EndDate":fields.DateTime
})

requestSchema = RequestSchema(many=True)
request = api.model("Request", {
    "RequestId":fields.Integer,
    "RequestReason": fields.String,
    "UnitsNeeded": fields.Integer,
    "TotalDonation": fields.Integer,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "CreatedAt": fields.DateTime,
    "UpdatedAt": fields.DateTime

})

addressSchema = AddressSchema(many=True)
address = api.model("Address", {
    "State": fields.String,
    "City": fields.String,
    "Subcity": fields.String,
    "Woreda": fields.String,
    "Kebele": fields.String,
    "Zone": fields.String,
    "AddressLine": fields.String,
    "PhoneNumber": fields.String
})

donationCenterSchema = DonationCenterSchema(many=True)
donationCenter = api.model("DonationCenter", {
    "DonationCenterName": fields.String,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "AppointmentDescription": fields.String
})

bloodTypeSchema = BloodTypeSchema(many=True)
bloodTypeSchema = api.model("Blood Type", {
    "BloodTypeName": fields.String,
    "BloodTypeDescription": fields.String,
})

emergencyContactSchema = EmergencyContactSchema()
emergencyContact = api.model("EmergencyContact", {
    "ContactName": fields.String,
    "ContactPhone": fields.String
})
