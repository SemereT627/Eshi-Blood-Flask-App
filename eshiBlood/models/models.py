from sqlalchemy import Enum
from eshiBlood import db
from eshiBlood.models.enums import *


class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column("AppointmentId", db.Integer, primary_key=True)
    StartDate = db.Column("StartDate", db.Date)
    EndDate = db.Column("EndDate", db.Date)
    StartTime = db.Column("StartTime", db.Date)
    EndTime = db.Column("EndTime", db.Date)
    Status = db.Column("Status", Enum(Status))
    AppointmentDescription = db.Column("AppointmentDescription", db.String)
    DonationCenter = db.Column('DonationCenter', db.Integer, db.ForeignKey(
        'DonationCenter.DonationCenterId'))


# directAppointment
# class DirectAppointment(db.Model):


# event
class Event(db.Model):
    __tablename__ = "Event"
    EventId = db.Column("EventId", db.Integer, primary_key=True)
    EventName = db.Column("EventName", db.String)
    EventGoal = db.Column("EventGoal", db.String)
    EventOrganizer = db.Column("EventOrganizer", db.Integer,
                               db.ForeignKey("User.UserId"))


# request
class Request(db.Model):
    __tablename__ = "Request"

    RequestId = db.Column("RequestId", db.Integer, primary_key=True)
    UnitsNeeded = db.Column("UnitsNeeded", db.Integer)
    RequestReason = db.Column("RequestReason", db.String)
    Address = db.Column("Address", db.Integer,
                        db.ForeignKey("Address.AddressId"))
    BloodType = db.Column("BloodType", db.Integer,
                          db.ForeignKey("BloodType.BloodTypeId"))

# address


class Address(db.Model):
    __tablename__ = "Address"
    AddressId = db.Column("AddressId", db.Integer, primary_key=True)
    State = db.Column("State", db.String)
    City = db.Column("City", db.String)
    SubCity = db.Column("SubCity", db.String)
    Woreda = db.Column("Woreda", db.String)
    Kebele = db.Column("Kebele", db.String)
    Zone = db.Column("Zone", db.String)
    AddressLine = db.Column("AddressLine", db.String)
    PostCode = db.Column("PostCode", db.String)
    PhoneNumber = db.Column("PhoneNumber", db.String)
    Email = db.Column("Email", db.String)


# donationcenter


class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column(
        "DonationCenterId", db.Integer, primary_key=True)
    Address = db.Column("AddressId", db.Integer,
                        db.ForeignKey("Address.AddressId"))
    DonationCenterName = db.Column("DonationCenterName", db.String)
    Status = db.Column("Status", Enum(Status))
    UpdatedBy = db.Column("UpdatedBy", db.Integer,
                          db.ForeignKey("User.UserId"))


# timeslot
class TimeSlot(db.Model):
    __tablename__ = "TimeSlot"
    TimeSlotId = db.Column("TimeSlotId", db.Integer, primary_key=True)
    Weekday = db.Column("Weekday", Enum(WeekDay))
    StartTime = db.Column("StartTime", db.Date)
    EndTime = db.Column("EndTime", db.Date)
    DonationCenter = db.Column("DonationCenter", db.Integer, db.ForeignKey(
        "DonationCenter.DonationCenterId"))


# bloodtypes
class BloodType(db.Model):
    __tablename__ = "BloodType"

    BloodTypeId = db.Column("BloodTypeId", db.Integer, primary_key=True)
    BloodTypeName = db.Column("BloodTypeName", db.String)
    BloodTypeDescription = db.Column("BloodTypeDescription", db.String)
    BloodTypeCreatedAt = db.Column("BloodTypeCreatedAt", db.String)
    BloodTypeUpdatedAt = db.Column("BloodTypeUpdatedAt", db.String)


# emergencycontact
class EmergencyContact(db.Model):
    __tablename__ = "EmergencyContact"
    EmergencyContactId = db.Column(
        "EmergencyContactId", db.Integer, primary_key=True)
    ContactName = db.Column("ContactName", db.String)
    ContactPhone = db.Column("ContactPhone", db.String)
    BloodType = db.Column("BloodType", db.Integer,
                          db.ForeignKey("BloodType.BloodTypeId"))
# user


class User(db.Model):
    __tablename__ = "User"

    UserId = db.Column("UserId", db.Integer, primary_key=True)
    FirstName = db.Column("FirstName", db.String)
    LastName = db.Column("LastName", db.String)
    UserName = db.Column("UserName", db.String)
    BirthDate = db.Column("BirthDate", db.Date)
    RegisteredAt = db.Column("RegisteredAt", db.Date)
    CreatedAt = db.Column("CreatedAt", db.Date)
    UpdatedAt = db.Column("UpdatedAt", db.Date)
    Gender = db.Column("Gender", Enum(Gender))
    check = db.Column("Check", db.String)

    MartialStatus = db.Column("MartialStatus",Enum(MartialStatus))
    BloodType = db.Column("BloodType", db.Integer,
                          db.ForeignKey("BloodType.BloodTypeId"))
    Address = db.Column("Address", db.Integer,
                        db.ForeignKey("Address.AddressId"))
    # Appointments = db.Column("Appointments",db.Integer, db.ForeignKey("Appointment.AppointmentId"))


# usercredential
class UserCredential(db.Model):
    __tablename__ = "UserCredential"
    UserCredentialId = db.Column("UserId", db.Integer, primary_key=True)
    Email = db.Column("FirstName", db.String)
    PhoneNumber = db.Column("PhoneNumber", db.String)
    Password = db.Column("Password", db.String)

# userrole


class UserRole(db.Model):
    __tablename__ = "UserRole"
    UserRoleId = db.Column("UserRoleId", db.Integer, primary_key=True)
    RoleName = db.Column("UserRoleName", db.Integer)
    User = db.Column("User", db.Integer, db.ForeignKey("User.UserId"))

