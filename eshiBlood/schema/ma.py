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
        fields = ("StartDate", "EndDate", "StartTime", "EndTime",
                  "Status", "AppointmentDescription", "DonationCenter")
        model = Appointment


class EventSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)
    class Meta:
        fields = ("EventName", "EventGoal", "EventOrganizer",
                  "TotalDonations", "Status", "CreatedAt", "UpdatedAt", "UpdatedBy")
        model = Event


class RequestSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)
    class Meta:
        fields = ("RequestReason", "UnitsNeeded", "BloodType",
                  "TotalDonation", "Status", "CreatedAt", "UpdatedAt", "UpdatedBy")
        model = Request


class AddressSchema(ma.Schema):
    class Meta:
        fields = ("State", "City", "Subcity", "Woreda",
                  "Kebele", "Zone", "AddressLine", "PhoneNumber")
        model = Address


class DonationCenterSchema(ma.Schema):
    Status = EnumField(Status, by_value=True)
    class Meta:
        fields = ("Address", "DonationCenterName", "Status", "UpdatedBy")
        model = DonationCenter

# Timeslot

class BloodTypeSchema(ma.Schema):
    class Meta:
        fields = ("BloodTypeName", "BloodTypeDescription")
        model = BloodType


class EmergencyContactSchema(ma.Schema):
    class Meta:
        fields = ("ContactName","ContactPhone","BloodType")
        model = EmergencyContact

# class DonationHistorySchema(ma.Schema):
#     class Meta:
#         fields = ("CreatedAt","AppointmentId")


userSchema = UserSchema()
user = api.model("User", {
    "FirstName": fields.String,
    "LastName": fields.String,
    "UserName": fields.String,
    "BirthDate": fields.DateTime,
    "Gender": fields.String,
    "MaritalStatus": fields.String,
})


userCredentialSchema = UserCredentialSchema()
userCredential = api.model("UserCredential", {
    'Email': fields.String('Your Email'),
    'Password': fields.String('Password')
})


appointmentSchema = AppointmentSchema(many=True)
appointment = api.model("Appointment", {
    "StartDate": fields.DateTime,
    "EndDate": fields.DateTime,
    "StartTime": fields.DateTime,
    "EndTime": fields.DateTime,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "AppointmentDescription": fields.String
})

eventSchema = EventSchema(many=True)
event = api.model("Event", {
    "EventName": fields.String,
    "EventGoal": fields.String,
    "EventOrganizer": fields.Integer,
    "TotalDonations": fields.Integer,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "CreatedAt": fields.DateTime,
    "UpdatedAt": fields.DateTime,
    "UpdatedBy": fields.Integer
})

requestSchema = RequestSchema(many=True)
request = api.model("Request", {
    "RequestReason": fields.String,
    "UnitsNeeded": fields.Integer,
    "TotalDonation": fields.Integer,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "CreatedAt": fields.DateTime,
    "UpdatedAt": fields.DateTime,
    "UpdatedBy": fields.Integer

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
    "Address": fields.String,
    "DonationCenterName": fields.String,
    "Status": fields.String(description="The object type", enum=["Active", "Pending", "Closed"]),
    "AppointmentDescription": fields.String
})

bloodTypeSchema = BloodTypeSchema()
bloodTypeSchema = api.model("Blood Type",{
    "BloodTypeName":fields.String,
    "BloodTypeDescription":fields.String,
})

emergencyContactSchema = EmergencyContactSchema()
emergencyContact = api.model("EmergencyContact",{
    "ContactName":fields.String,
    "ContactPhone":fields.String
})