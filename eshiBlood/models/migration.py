
from flask_sqlalchemy import SQLAlchemy
from flask_app import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import sys
from sqlalchemy import Integer,Enum

# ##############  user import #############
from models.enums import *

#configure app to enable it to interact with your database
#format: 'postgresql://user:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yagami:deathnote@localhost/e_flask'

#To maintain migrations
db=SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Database relational models based on flask-SQLAlchemy ORM syntax
# class Customer(db.Model):

# 	__tablename__ = "customer"

# 	id=db.Column('customer_id',db.String(20),primary_key=True)
# 	first_name=db.Column('first_name',db.String(20))
# 	last_name=db.Column('last_name',db.String(20))
# 	loginid=db.Column('loginid',db.String(10),unique=True)
# 	passwd=db.Column('passwd',db.String(20),unique=True)
# 	contact_num=db.Column('contact_num',db.String)

# class order(db.Model):

# 	__tablename__ = "aboutorder"		
	
# 	id=db.Column('order_id',db.String(20),primary_key=True)
# 	order_num=db.Column('order_num',db.Integer)
# 	ship_via=db.Column('ship_via',db.String(20))
# 	shipper_ID=db.Column('shipper_ID',db.String(20))
# 	order_date=db.Column('order_date',db.Date)
# 	shipped_date=db.Column('shipped_date',db.Date)

# 	customer_ID=db.Column('customer',db.String(20),db.ForeignKey('customer.customer_id'))

class Appointment(db.Model):
    __tablename__ = "Appointment"

    AppointmentId = db.Column("AppointmentId",db.Integer , primary_key=True)
    StartDate = db.Column("StartDate",db.Date)
    EndDate = db.Column("EndDate",db.Date)
    StartTime = db.Column("StartTime",db.Date)
    EndTime = db.Column("EndTime",db.Date)
    Status = db.Column("Status",Enum(Status))
    AppointmentDescription = db.Column("AppointmentDescription",db.String)
    DonationCenter=db.Column('DonationCenter',db.Integer,db.ForeignKey('DonationCenter.DonationCenterId'))

class DonationCenter(db.Model):
    __tablename__ = "DonationCenter"

    DonationCenterId = db.Column("DonationCenterId",db.Integer,primary_key=True)
    Address = db





class Address(db.Model):
    AddressId = db.Column("AddressId", db.Integer, primary_key=True)
    State = db.Column




if __name__ == '__main__':
    manager.run()