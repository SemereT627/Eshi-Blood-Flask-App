from sqlalchemy import Enum
from eshiBlood import db
from eshiBlood.models.enums import *


class User(db.Model):
    __tablename__ = "User"

    UserId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20), nullable=False)
    LastName = db.Column(db.String(20))
    UserName = db.Column(db.String(20))
    BirthDate = db.Column(db.Date)
    RegisteredAt = db.Column(db.Date)
    CreatedAt = db.Column(db.Date)
    UpdatedAt = db.Column(db.Date)
    Gender = db.Column(db.String)
    check = db.Column(db.String(20))
    MartialStatus = db.Column(db.String(20))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    # Appointments = db.Column("Appointments",db.Integer, db.ForeignKey("Appointment.AppointmentId"))

# usercredential
class UserCredential(db.Model):
    __tablename__ = "UserCredential"
    UserCredentialId = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(20),nullable=False)
    Password = db.Column(db.String(20),nullable=False)


# userrole


class UserRole(db.Model):
    __tablename__ = "UserRole"
    UserRoleId = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.Integer)
    User = db.Column(db.Integer, db.ForeignKey("User.UserId"))


class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.Date)
    EndDate = db.Column(db.Date)
    StartTime = db.Column(db.Date)
    EndTime = db.Column(db.Date)
    Status = db.Column(Enum(Status))
    AppointmentDescription = db.Column(db.String(20))
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        'DonationCenter.DonationCenterId'))


# directAppointment
# class DirectAppointment(db.Model):


# event
class Event(db.Model):
    __tablename__ = "Event"
    EventId = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String(20))
    EventGoal = db.Column(db.String(20))
    EventOrganizer = db.Column(db.Integer, db.ForeignKey("User.UserId"))


# request
class Request(db.Model):
    __tablename__ = "Request"

    RequestId = db.Column(db.Integer, primary_key=True)
    UnitsNeeded = db.Column(db.Integer)
    RequestReason = db.Column(db.String(20))
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))

# address


class Address(db.Model):
    __tablename__ = "Address"
    AddressId = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String(20))
    City = db.Column(db.String(20))
    SubCity = db.Column(db.String(20))
    Woreda = db.Column(db.String(20))
    Kebele = db.Column(db.String(20))
    Zone = db.Column(db.String(20))
    AddressLine = db.Column(db.String(20))
    PostCode = db.Column(db.String(20))
    PhoneNumber = db.Column(db.String(20))
    Email = db.Column(db.String(20))


# donationcenter


class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    DonationCenterName = db.Column(db.String(20))
    Status = db.Column(Enum(Status))
    UpdatedBy = db.Column(db.Integer, db.ForeignKey("User.UserId"))


# timeslot
class TimeSlot(db.Model):
    __tablename__ = "TimeSlot"
    TimeSlotId = db.Column(db.Integer, primary_key=True)
    Weekday = db.Column(Enum(WeekDay))
    StartTime = db.Column(db.Date)
    EndTime = db.Column(db.Date)
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        "DonationCenter.DonationCenterId"))


# bloodtypes
class BloodType(db.Model):
    __tablename__ = "BloodType"
    BloodTypeId = db.Column(db.Integer, primary_key=True)
    BloodTypeName = db.Column(db.String(20))
    BloodTypeDescription = db.Column(db.String(20))
    BloodTypeCreatedAt = db.Column(db.String(20))
    BloodTypeUpdatedAt = db.Column(db.String(20))


# emergencycontact
class EmergencyContact(db.Model):
    __tablename__ = "EmergencyContact"
    EmergencyContactId = db.Column(db.Integer, primary_key=True)
    ContactName = db.Column(db.String(20))
    ContactPhone = db.Column(db.String(20))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
# user
