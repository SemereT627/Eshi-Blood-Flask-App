
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import sys

from sqlalchemy import create_engine
from sqlalchemy import (ForeignKey, Boolean, Table,Column,Integer,Numeric,String,Date,Enum)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship,backref
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

# ##############  user import #############
# from models.enums import *
import sys
sys.path.append("./")
from enums import *




# #########################################
app = Flask(__name__)
#configure app to enable it to interact with your database
#format: 'postgresql://user:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/eshiblood'

#To maintain migrations
# db=SQLAlchemy.create_engine( 'postgresql://postgres:Abyssinia@0001@localhost/eshiblood',)
# db = sqlalchemy(app)
engine = create_engine('postgresql://postgres:root@localhost:5432/eshiblood')
# db = scoped_session(sessionmaker(bind=engine))
# migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)




# Database relational models based on flask-SQLAlchemy ORM syntax
# class Customer(base):

# 	__tablename__ = "customer"

# 	id=Column('customer_id',String(20),primary_key=True)
# 	first_name=Column('first_name',String(20))
# 	last_name=Column('last_name',String(20))
# 	loginid=Column('loginid',String(10),unique=True)
# 	passwd=Column('passwd',String(20),unique=True)
# 	contact_num=Column('contact_num',String())

# class order(base):

# 	__tablename__ = "aboutorder"		
	
# 	id=Column('order_id',String(20),primary_key=True)
# 	order_num=Column('order_num',Integer())
# 	ship_via=Column('ship_via',String(20))
# 	shipper_ID=Column('shipper_ID',String(20))
# 	order_date=Column('order_date',Date)
# 	shipped_date=Column('shipped_date',Date)

# 	customer_ID=Column('customer',String(20),ForeignKey('customer.customer_id'))



# appointment
class Appointment(base):
    __tablename__ = "Appointment"

    AppointmentId = Column("AppointmentId",Integer() , primary_key=True)
    StartDate = Column("StartDate",Date)
    EndDate = Column("EndDate",Date)
    StartTime = Column("StartTime",Date)
    EndTime = Column("EndTime",Date)
    Status = Column("Status",Enum(Status))
    AppointmentDescription = Column("AppointmentDescription",String())
    DonationCenter=Column('DonationCenter',Integer(),ForeignKey('DonationCenter.DonationCenterId'))


# directAppointment
# class DirectAppointment(base):
    

# event
class Event(base):
    __tablename__ = "Event"
    EventId = Column("EventId",Integer(),primary_key=True)
    EventName = Column("EventName",String())
    EventGoal = Column("EventGoal",String())
    EventOrganizer = Column("EventOrganizer",Integer(), ForeignKey("User.UserId"))
    


# request
class Request(base):
    __tablename__ = "Request"

    RequestId = Column("RequestId",Integer(),primary_key=True)
    UnitsNeeded = Column("UnitsNeeded",Integer())
    RequestReason = Column("RequestReason",String())
    Address = Column("Address",Integer(),ForeignKey("Address.AddressId"))
    BloodType = Column("BloodType",Integer(),ForeignKey("BloodType.BloodTypeId"))

# address

class Address(base):
    __tablename__ = "Address"
    AddressId = Column("AddressId", Integer(), primary_key=True)
    State = Column("State",String())
    City = Column("City",String())
    SubCity = Column("SubCity",String())
    Woreda = Column("Woreda",String())
    Kebele = Column("Kebele",String())
    Zone = Column("Zone",String())
    AddressLine = Column("AddressLine",String())
    PostCode = Column("PostCode",String())
    PhoneNumber = Column("PhoneNumber",String())
    Email = Column("Email",String())

# basemodel

# donationcenter

class DonationCenter(base):
    __tablename__ = "DonationCenter"

    DonationCenterId = Column("DonationCenterId",Integer(),primary_key=True)
    Address = Column("AddressId",Integer(), ForeignKey("Address.AddressId"))
    DonationCenterName = Column("DonationCenterName",String())
    Status = Column("Status",Enum(Status))
    UpdatedBy = Column("UpdatedBy",Integer(),ForeignKey("User.UserId"))


# timeslot
class TimeSlot(base):
    __tablename__ = "TimeSlot"
    TimeSlotId = Column("TimeSlotId",Integer(), primary_key = True)
    Weekday = Column("Weekday",Enum(WeekDay))
    StartTime = Column("StartTime",Date)
    EndTime = Column("EndTime",Date)
    DonationCenter = Column("DonationCenter",Integer(), ForeignKey("DonationCenter.DonationCenterId"))
     


# bloodtypes
class BloodType(base):
    __tablename__ = "BloodType"

    BloodTypeId = Column("BloodTypeId",Integer(),primary_key = True)
    BloodTypeName = Column("BloodTypeName",String())
    BloodTypeDescription = Column("BloodTypeDescription",String())
    BloodTypeCreatedAt = Column("BloodTypeCreatedAt",String())
    BloodTypeUpdatedAt = Column("BloodTypeUpdatedAt",String())


# emergencycontact
class EmergencyContact(base):
    __tablename__ = "EmergencyContact"
    EmergencyContactId = Column("EmergencyContactId",Integer(),primary_key=True)
    ContactName = Column("ContactName",String())
    ContactPhone = Column("ContactPhone",String())
    BloodType = Column("BloodType",Integer(),ForeignKey("BloodType.BloodTypeId"))
# user
class User(base):
    __tablename__ = "User"

    UserId = Column("UserId",Integer(),primary_key=True)
    FirstName=  Column("FirstName",String())
    LastName = Column("LastName",String())
    UserName = Column("UserName",String())
    BirthDate = Column("BirthDate",Date)
    RegisteredAt = Column("RegisteredAt",Date)
    CreatedAt = Column("CreatedAt",Date)
    UpdatedAt = Column("UpdatedAt",Date)
    Gender = Column("Gender",Enum(Gender))
    
    MartialStatus = Column("MartialStatus",Enum(MartialStatus))
    BloodType = Column("BloodType",Integer(), ForeignKey("BloodType.BloodTypeId"))
    Address = Column("Address",Integer(), ForeignKey("Address.AddressId"))
    # Appointments = Column("Appointments",Integer(), ForeignKey("Appointment.AppointmentId"))




# usercredential
class UserCredentail(base):
    __tablename__ = "UserCredential"
    UserCredentialId = Column("UserId",Integer(),primary_key=True)
    Email=  Column("FirstName",String())
    PhoneNumber = Column("PhoneNumber",String())
    Password = Column("Password",String())

# userrole

class UserRole(base):
    __tablename__ = "UserRole"
    UserRoleId = Column("UserRoleId",Integer(),primary_key=True)
    RoleName = Column("UserRoleName",Integer())
    User = Column("User",Integer(),ForeignKey("User.UserId"))
    
  







if __name__ == '__main__':
    # manager.run()
    base.metadata.create_all(engine)