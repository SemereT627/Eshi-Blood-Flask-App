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
    Address = relationship("Address",backref="addressbackref",uselist=False )
    Appointments = relationship("Appointment",backref="Appointment" )
    DonationCenter = relationship("DonationCenter",backref="userDonationCenterBackref",uselist=False)


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
    
    User = db.Column(db.Integer,db.ForeignKey("User.UserId"),unique=True)

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


class BloodType(db.Model):
    __tablename__ = "BloodType"
    BloodTypeId = db.Column(db.Integer, primary_key=True)
    BloodTypeName = db.Column(db.String)
    BloodTypeDescription = db.Column(db.String)
    BloodTypeCreatedAt = db.Column(db.String)
    BloodTypeUpdatedAt = db.Column(db.String)
    Users = relationship("User", backref="user")

