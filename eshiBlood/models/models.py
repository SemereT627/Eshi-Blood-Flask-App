from enum import unique
from sqlalchemy import Enum, DateTime
from sqlalchemy.orm import backref, relationship
from eshiBlood import db
from eshiBlood.models.enums import *

Request_BloodType_Association = db.Table("Request_BloodType_Association", db.Model.metadata,
                                         db.Column("BloodType", db.Integer, db.ForeignKey(
                                             "BloodType.BloodTypeId")),
                                         db.Column("Request", db.Integer, db.ForeignKey("Request.RequestId")))

# User


class User(db.Model):
    __tablename__ = "User"
    UserId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String, nullable=False)
    LastName = db.Column(db.String)
    UserName = db.Column(db.String)
    Gender = db.Column(Enum(Gender))
    BirthDate = db.Column(DateTime)
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    MartialStatus = db.Column(Enum(MartialStatus))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    Appointments = relationship("Appointment", backref="Appointment")
    DonationCenters = relationship(
        "DonationCenter", backref="userDonationCenterBackref")
    Events = relationship("Event", backref="userEventBackref")
    UserCredential = db.Column(db.Integer, db.ForeignKey(
        "UserCredential.UserCredentialId"))
    UserRole = db.Column(db.Integer, db.ForeignKey("UserRole.UserRoleId"))
    EmergencyContact = db.Column(db.Integer, db.ForeignKey("EmergencyContact.EmergencyContactId"))

# UserCredential
class UserCredential(db.Model):
    __tablename__ = "UserCredential"
    UserCredentialId = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)
    User = relationship(
        "User", backref="UserUserCredentialBackref", uselist=False)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(Email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(UserCredentialId=_id).first()

    # helps to save to database -- not to write add and commit everytime
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


# UserRole
class UserRole(db.Model):
    __tablename__ = "UserRole"
    UserRoleId = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(Enum(Role))
    Users = relationship("User", backref="UserRoleUserBackref")


class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column(db.Integer, primary_key=True)
    # StartDate = db.Column(DateTime)
    # EndDate = db.Column(DateTime)
    # StartTime = db.Column(DateTime)
    # EndTime = db.Column(DateTime)
    Status = db.Column(Enum(Status))
    AppointmentDescription = db.Column(db.String)
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        'DonationCenter.DonationCenterId'))
    Discriminator = db.Column(db.String)
    DiscriminatorId = db.Column(db.Integer)
    User = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)


# Event
class Event(db.Model):
    __tablename__ = "Event"
    EventId = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String)
    EventGoal = db.Column(db.String)
    EventOrganizer = db.Column(db.Integer, db.ForeignKey("User.UserId"))
    TotalDonations = db.Column(db.Integer)
    Status = db.Column(Enum(Status))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    # CreatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    # UpdatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))


# Request
class Request(db.Model):
    __tablename__ = "Request"

    RequestId = db.Column(db.Integer, primary_key=True)
    UnitsNeeded = db.Column(db.Integer)
    RequestReason = db.Column(db.String)
    BloodTypes = relationship(
        "BloodType", secondary=Request_BloodType_Association, back_populates="Requests")
    TotalDonation = db.Column(db.Integer)
    Status = db.Column(Enum(Status))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    CreatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    # UpdatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    # one to many blood type

# Address


class Address(db.Model):
    __tablename__ = "Address"
    AddressId = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String)
    City = db.Column(db.String)
    Woreda = db.Column(db.String)
    Kebele = db.Column(db.String)
    Zone = db.Column(db.String)
    AddressLine = db.Column(db.String)
    PostCode = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    User = relationship("User",backref="userAddressBackref",uselist=False)
    Request = relationship("Request",backref="RequestBackref",uselist=False)

# DonationCenter
class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    DonationCenterName = db.Column(db.String)
    Status = db.Column(Enum(Status))
    UpdatedBy = db.Column(
        db.Integer, db.ForeignKey("User.UserId"), unique=True)
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    Appointments = relationship("Appointment", backref="DonationCenterBackRef")
    TimeSlots = relationship("TimeSlot", backref="TimeSlotBackref")


# Timeslot
class TimeSlot(db.Model):
    __tablename__ = "TimeSlot"
    TimeSlotId = db.Column(db.Integer, primary_key=True)
    Weekday = db.Column(Enum(WeekDay))
    StartTime = db.Column(DateTime)
    EndTime = db.Column(DateTime)
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        "DonationCenter.DonationCenterId"))


# bloodtypes
class BloodType(db.Model):
    __tablename__ = "BloodType"
    BloodTypeId = db.Column(db.Integer, primary_key=True)
    BloodTypeName = db.Column(db.String)
    BloodTypeDescription = db.Column(db.String)
    BloodTypeCreatedAt = db.Column(db.String)
    BloodTypeUpdatedAt = db.Column(db.String)
    Users = relationship("User", backref="userBloodTypeBackref")
    Requests = relationship(
        "Request", secondary=Request_BloodType_Association, back_populates="BloodTypes")
    EmergencyContacts = relationship(
        "EmergencyContact", backref="EmergencyContactBloodTypeBackref")

# emergencycontact


class EmergencyContact(db.Model):
    __tablename__ = "EmergencyContact"
    EmergencyContactId = db.Column(db.Integer, primary_key=True)
    ContactName = db.Column(db.String)
    ContactPhone = db.Column(db.String)
    User = relationship("User",backref="emeregencycontactuserbackref",uselist=False)
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
# user


class DonationHistory(db.Model):
    __tablename__ = "DonationHistory"
    DonationCenterId = db.Column(db.Integer, primary_key=True)
    CreatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    AppointmentId = db.Column(
        db.Integer, db.ForeignKey("Appointment.AppointmentId"))
    UserId = db.Column(db.Integer, db.ForeignKey("User.UserId"))
    NurseId = db.Column(db.Integer, db.ForeignKey("User.UserId"))
