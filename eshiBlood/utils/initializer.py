from datetime import datetime
from threading import Event
from eshiBlood.models import models
from eshiBlood import db
from eshiBlood.models.enums import *

def initializeBloodTypes():
    # bloodtype,
    Anegative = models.BloodType()
    # aType.id = 1
    Anegative.BloodTypeName = "A-"

    # bloodtype,
    Bnegative = models.BloodType()
    # aType.id = 1
    Bnegative.BloodTypeName = "B-"

    # bloodtype,
    ABnegative = models.BloodType()
    # aType.id = 1
    ABnegative.BloodTypeName = "AB-"

    # bloodtype,
    Apositive = models.BloodType()
    # aType.id = 1
    Apositive.BloodTypeName = "A+"

    # bloodtype,
    Bpositive = models.BloodType()
    # aType.id = 1
    Bpositive.BloodTypeName = "B+"

    # bloodtype,
    ABpositive = models.BloodType()
    # aType.id = 1
    ABpositive.BloodTypeName = "AB+"

    # bloodtype,
    Opositive = models.BloodType()
    # aType.id = 1
    Opositive.BloodTypeName = "O+"

    # bloodtype,
    Onegative = models.BloodType()
    # aType.id = 1
    Onegative.BloodTypeName = "O-"
    db.session.add_all([Apositive,Anegative,Bnegative,Bpositive,ABnegative,ABpositive,Opositive,Onegative])
    db.session.commit()
    print("Blood types initialized")
def initializeRoles():
    # role,
    superAdminRole = models.UserRole()
    # superAdminRole.UserRoleId = 4
    superAdminRole.RoleName = Role.SuperAdmin

    adminRole = models.UserRole()
    # adminRole.UserRoleId = 1
    adminRole.RoleName = Role.Admin

    donorRole = models.UserRole()
    # donorRole.UserRoleId = 2
    donorRole.RoleName = Role.Donor

    nurseRole = models.UserRole()
    # nurseRole.UserRoleId = 3
    nurseRole.RoleName = Role.Nurse
    db.session.add_all([superAdminRole,adminRole, donorRole, nurseRole])
    db.session.commit()
    print("roles initialized")
def initializeSuper():
    # oType.BloodTypeName = "O"
    # # users
    superAdmin = models.User()
    # superAdmin.UserId = 1
    superAdmin.FirstName = "abebe"
    superAdminRole = models.UserRole.query.filter_by(RoleName="SuperAdmin").first()
    superAdminRole.Users.append(superAdmin)

    superAdminCredential= models.UserCredential()
    superAdminCredential.UserCredentialId=1
    superAdminCredential.Email="abebe@email.com"
    superAdminCredential.Password = "mypass"

    superAdminCredential.User = superAdmin
    try:
        db.session.add_all([superAdmin,superAdminCredential])
        db.session.commit()
    except Exception:
        pass
    print("super initialized")

def initializeDonors():
    db.session.rollback()
    
    role = models.UserRole.query.filter_by(RoleName = "Donor").first()
    

    donor1 = models.User()
    # donor1.UserId = 9
    donor1.FirstName = "Abrham"
    donor1.LastName = "Tesfaye"
    

    typeA = models.BloodType.query.filter_by(BloodTypeName="A+").first()
    typeB = models.BloodType.query.filter_by(BloodTypeName="B-").first()
    typeAB = models.BloodType.query.filter_by(BloodTypeName="AB+").first()
    

    donor2 = models.User()
    # donor2.UserId = 10
    donor2.FirstName = "Michael"
    donor2.LastName = "Solomon"
    

    donor3 = models.User()
    # donor3.UserId = 11
    donor3.FirstName = "Abenezer"
    donor3.LastName = "Atnafu"
    

    userCred1 = models.UserCredential()
    # userCred1.UserCredentialId = 9
    userCred1.Email = "abrham@gmail.com"
    userCred1.Password = "pass123"

        
    userCred2 = models.UserCredential()
    # userCred2.UserCredentialId = 10
    userCred2.Email = "michael@gmail.com"
    userCred2.Password="pass124"

    userCred3 = models.UserCredential()
    # userCred3.UserCredentialId = 11
    userCred3.Email = "abenezer@gmail.com"
    userCred3.Password="pass324"
    


    userCred1.User = donor1
    userCred2.User = donor2
    userCred3.User = donor3
    

    

    role.Users.append(donor1)
    role.Users.append(donor2)
    role.Users.append(donor3)
    

    typeA.Users.append(donor1)#TODO
    print("1")
    typeB.Users.append(donor2)
    typeAB.Users.append(donor3)

    db.session.add_all([donor1,donor2,donor3,userCred1,userCred2,userCred3])
    db.session.commit()
    print("donors initialized") 
    # try:
    
    #     db.session.add_all([donor1,donor2,donor3,userCred1,userCred2,userCred3])
    #     db.session.commit()
    #     print("donors initialized")
    
    # except:
    #     print("already initialized")
    
    
def initializeAppointments():
    
    db.session.rollback()
    appt1 = models.Appointment()
    appt2 = models.Appointment()
    appt3 = models.Appointment()
    # appt4 = models.Appointment()
    
    # appt1.AppointmentId = 1
    # appt2.AppointmentId = 2
    # appt3.AppointmentId = 3
    # appt4.AppointmentId = 4

    appt1.UpdatedAt = datetime.now()
    appt2.UpdatedAt = datetime.now()
    appt3.UpdatedAt = datetime.now()
    # appt4.UpdatedAt = datetime.now()

    appt1.AppointmentDescription = "desc 1"
    appt2.AppointmentDescription = "desc 2"
    appt3.AppointmentDescription = "desc 3"
    # appt4.AppointmentDescription = "desc 4"

    
    
    u11 = models.User.query.filter_by(FirstName = "Abrham").first()
    u9 = models.User.query.filter_by(FirstName = "Michael").first()
    u10 = models.User.query.filter_by(FirstName = "Abenezer").first()
    # u8 = models.User.query.filter_by(UserId = 8).first()
    print(u11.FirstName)

    u11.Appointments.append(appt1)
    u9.Appointments.append(appt2)
    u10.Appointments.append(appt3)
    # u8.Appointments.append(appt4)
    

    db.session.add_all([appt1,appt2,appt3])
    db.session.commit()
    print("appointments initialized")

def initializeEvents():
    print("event initializer")
    db.session.rollback()
    ev1 = models.Event()
    # ev1.EventId = 1
    ev2 = models.Event()
    # ev2.EventId = 2
    ev3 = models.Event()
    # ev3.EventId = 3

    u11 = models.User.query.filter_by(FirstName = "Abrham").first()
    u9 = models.User.query.filter_by(FirstName = "Michael").first()
    u10 = models.User.query.filter_by(FirstName = "Abenezer").first()

    u9.Events.append(ev1)
    u10.Events.append(ev2)
    u11.Events.append(ev3)

    ev1.EventName = "Pepsi event"
    ev2.EventName = "bunna blood donations"
    ev3.EventName = "rotract blood donating session"

    db.session.add_all([ev1,ev2,ev3])
    db.session.commit()
    print("events initialized")


def initializeNurses():
    db.session.rollback()
    nurse1 = models.User()
    nurse2 = models.User()
    nurse1.FirstName = "nurse 1"
    nurse2.FirstName = "nurse 2"

    # nurse1.UserId = 12
    # nurse2.UserId = 13
    nurseRole = models.UserRole.query.filter_by(RoleName = "Nurse").first()

    userCred1 = models.UserCredential()
    userCred2 = models.UserCredential()

    userCred1.Email = "nurse1@gmail.com"
    userCred2.Email = "nurse2@gmail.com"

    userCred1.Password = "nurse1password"
    userCred2.Password = "nurse2password"

    userCred1.User = nurse1
    userCred2.User = nurse2

    nurseRole.Users.append(nurse1)
    nurseRole.Users.append(nurse2)

    donationCenter1 = models.DonationCenter()
    donationCenter1.DonationCenterName="6 kilo center"
    donationCenter2 = models.DonationCenter()
    donationCenter2.DonationCenterName="mexico donator centor"

    nurse1.DonationCenters.append(donationCenter1)
    nurse2.DonationCenters.append(donationCenter2)

    db.session.add_all([nurse1,nurse2,userCred1,userCred2])
    db.session.commit()
    print("nurses initialized")
# def initializeAppointmentsThroughDonationCenters