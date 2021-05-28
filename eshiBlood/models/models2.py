from enum import unique
from sqlalchemy import Enum
from sqlalchemy.orm import backref,relationship
from eshiBlood import db
from eshiBlood.models.enums import *



class User(db.Model):
    __tablename__ = "User"

    UserId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String, nullable=False)
    LastName = db.Column(db.String)
    UserName = db.Column(db.String)
    BirthDate = db.Column(db.Date)
    RegisteredAt = db.Column(db.Date)
    CreatedAt = db.Column(db.Date)
    UpdatedAt = db.Column(db.Date)
    Gender = db.Column(Enum(Gender))
    MartialStatus = db.Column(Enum(MartialStatus))
    BloodType = db.Column(db.Integer,db.ForeignKey("BloodType.BloodTypeId"))
    # Address = relationship("Address",backref="addressbackref",uselist=False )
    Address = db.Column(db.Integer,db.ForeignKey("Address.AddressId"))
    Appointments = relationship("Appointment",backref="Appointment" )
    DonationCenters = relationship("DonationCenter",backref="userDonationCenterBackref")
    EmergencyContactName = db.Column(db.String)
    EmergencyContactPhone = db.Column(db.String)
    # EmergencyContactBloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
    Events = relationship("Event",backref="userEventBackref")
    UserCredential = db.Column(db.Integer,db.ForeignKey("UserCredential.UserCredentialId"))
    UserRole = db.Column(db.Integer,db.ForeignKey("UserRole.UserRoleId"))

class Address(db.Model):
    __tablename__ = "Address"
    AddressId = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String)
    City = db.Column(db.String)
    SubCity = db.Column(db.String)
    Woreda = db.Column(db.String)
    Kebele = db.Column(db.String)
    Zone = db.Column(db.String)
    AddressLine = db.Column(db.String)
    PostCode = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    Email = db.Column(db.String)
    
    # User = db.Column(db.Integer,db.ForeignKey("User.UserId"),unique=True)
    User = relationship("User",backref="userAddressBackref",uselist=False)
    Request = relationship("Request",backref="RequestBackref",uselist=False)

class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    StartTime = db.Column(db.Date)
    EndTime = db.Column(db.Date)
    Status = db.Column(Enum(Status))
    AppointmentDescription = db.Column(db.String)
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        'DonationCenter.DonationCenterId'))
    User = db.Column(db.Integer,db.ForeignKey("User.UserId"))

class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    DonationCenterName = db.Column(db.String)
    Status = db.Column(Enum(Status))
    # User/ owner/ head
    UpdatedBy = db.Column(db.Integer, db.ForeignKey("User.UserId"),unique=True)
    Appointments = relationship("Appointment",backref="DonationCenterBackRef")
    TimeSlots = relationship("TimeSlot",backref="TimeSlotBackref")


class BloodType(db.Model):
    __tablename__ = "BloodType"
    BloodTypeId = db.Column(db.Integer, primary_key=True)
    BloodTypeName = db.Column(db.String)
    BloodTypeDescription = db.Column(db.String)
    BloodTypeCreatedAt = db.Column(db.String)
    BloodTypeUpdatedAt = db.Column(db.String)
    Users = relationship("User", backref="user")

# timeslot
class TimeSlot(db.Model):
    __tablename__ = "TimeSlot"
    TimeSlotId = db.Column(db.Integer, primary_key=True)
    Weekday = db.Column(Enum(WeekDay))
    StartTime = db.Column(db.Date)
    EndTime = db.Column(db.Date)
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        "DonationCenter.DonationCenterId"))
class Request(db.Model):
    __tablename__ = "Request"

    RequestId = db.Column(db.Integer, primary_key=True)
    UnitsNeeded = db.Column(db.Integer)
    RequestReason = db.Column(db.String)
    Address = db.Column(db.Integer,db.ForeignKey("Address.AddressId"))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))


class Event(db.Model):
    __tablename__ = "Event"
    EventId = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String)
    EventGoal = db.Column(db.String)
    EventOrganizer = db.Column(db.Integer, db.ForeignKey("User.UserId"))

class UserCredential(db.Model):
    __tablename__ = "UserCredential"
    UserCredentialId = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String)
    Password = db.Column(db.String)
    User = relationship("User",backref="UserUserCredentialBackref",uselist=False)

class UserRole(db.Model):
    __tablename__ = "UserRole"
    UserRoleId = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.Integer)
    Users = relationship("User",backref="UserRoleUserBackref")



"""
------------Usage----------------------
User.Events = [Event]
User.Appointments = [Appointment]
User.DonationCenters=[DonationCenter]

Address.User = User
Address.Request = Request

DonationCenter.Appointments = [Appointments]
DonationCenter.TimeSlots = [TimeSlots]

UserCredential.User = User
UserRole.User = [User]

BloodType.Users = [User]

"""
