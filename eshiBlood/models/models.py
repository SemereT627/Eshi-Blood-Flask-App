from sqlalchemy import Enum, DateTime
from eshiBlood import db
from eshiBlood.models.enums import *


class User(db.Model):
    __tablename__ = "User"

    UserId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30), nullable=False)
    LastName = db.Column(db.String(30))
    UserName = db.Column(db.String(30))
    BirthDate = db.Column(DateTime)
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    Gender = db.Column(db.String)
    check = db.Column(db.String(30))
    MartialStatus = db.Column(db.String(30))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    # Appointments = db.Column("Appointments",db.Integer, db.ForeignKey("Appointment.AppointmentId"))

# usercredential


class UserCredential(db.Model):
    __tablename__ = "UserCredential"
    UserCredentialId = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(30), nullable=False)
    Password = db.Column(db.String(60), nullable=False)

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
# userrole


class UserRole(db.Model):
    __tablename__ = "UserRole"
    UserRoleId = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.Integer)
    User = db.Column(db.Integer, db.ForeignKey("User.UserId"))


class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(DateTime)
    EndDate = db.Column(DateTime)
    StartTime = db.Column(DateTime)
    EndTime = db.Column(DateTime)
    Status = db.Column(Enum(Status))
    AppointmentDescription = db.Column(db.String(30))
    DonationCenter = db.Column(db.Integer, db.ForeignKey(
        'DonationCenter.DonationCenterId'))
    Discriminator = db.Column(db.String)
    DiscriminatorId = db.Column(db.Integer)
    DonorId = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
# directAppointment
# class DirectAppointment(db.Model):


# event
class Event(db.Model):
    __tablename__ = "Event"
    EventId = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String(30))
    EventGoal = db.Column(db.String(30))
    EventOrganizer = db.Column(db.Integer, db.ForeignKey("User.UserId"))
    TotalDonations = db.Column(db.Integer)
    Status = db.Column(Enum(Status))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    CreatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    UpdatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
# request


class Request(db.Model):
    __tablename__ = "Request"

    RequestId = db.Column(db.Integer, primary_key=True)
    UnitsNeeded = db.Column(db.Integer)
    RequestReason = db.Column(db.String(30))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
    TotalDonation = db.Column(db.Integer)
    Status = db.Column(Enum(Status))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    CreatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    UpdatedBy = db.Column(db.Integer, db.ForeignKey('User.UserId'))
    # one to many blood type
# address


class Address(db.Model):
    __tablename__ = "Address"
    AddressId = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String(30))
    City = db.Column(db.String(30))
    SubCity = db.Column(db.String(30))
    Woreda = db.Column(db.String(30))
    Kebele = db.Column(db.String(30))
    Zone = db.Column(db.String(30))
    AddressLine = db.Column(db.String(30))
    PostCode = db.Column(db.String(30))
    PhoneNumber = db.Column(db.String(30))
    Email = db.Column(db.String(30)) #TBD


# donationcenter


class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.Integer, db.ForeignKey("Address.AddressId"))
    DonationCenterName = db.Column(db.String(30))
    Status = db.Column(Enum(Status))
    UpdatedBy = db.Column(db.Integer, db.ForeignKey("User.UserId"))
    CreatedAt = db.Column(DateTime)
    UpdatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)

# timeslot
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
    BloodTypeName = db.Column(db.String(30))
    BloodTypeDescription = db.Column(db.String(30))
    BloodTypeCreatedAt = db.Column(db.String(30))
    BloodTypeUpdatedAt = db.Column(db.String(30))


# emergencycontact
class EmergencyContact(db.Model):
    __tablename__ = "EmergencyContact"
    EmergencyContactId = db.Column(db.Integer, primary_key=True)
    ContactName = db.Column(db.String(30))
    ContactPhone = db.Column(db.String(30))
    BloodType = db.Column(db.Integer, db.ForeignKey("BloodType.BloodTypeId"))
# user


class DonationHistory(db.Model):
    __tablename__ = "DonationHistory"
    DonationCenterId = db.Column(db.Integer, primary_key=True)
    CreatedAt = db.Column(DateTime)
    IsDeleted = db.Column(db.Integer)
    AppointmentId = db.Column(db.Integer,db.ForeignKey("Appointment.AppointmentId"))
    UserId = db.Column(db.Integer,db.ForeignKey("User.UserId"))
    NurseId = db.Column(db.Integer,db.ForeignKey("User.UserId"))