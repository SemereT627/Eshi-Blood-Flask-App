from operator import mod

from flask_sqlalchemy import model
from eshiBlood.models import models
from eshiBlood import db
from eshiBlood.models.enums import Role


def initialize():
    # database initialize
    # super admin initialization
    superAdminRole = models.UserRole()
    superAdminRole.UserRoleId = 1
    superAdminRole.RoleName = Role.SuperAdmin
    # role,
    adminRole = models.UserRole()
    adminRole.UserRoleId = 2
    adminRole.RoleName = Role.Admin

    donorRole = models.UserRole()
    donorRole.UserRoleId = 3
    donorRole.RoleName = Role.Donor

    nurseRole = models.UserRole()
    nurseRole.UserRoleId = 4
    nurseRole.RoleName = Role.Nurse

    # bloodtype,
    aType = models.BloodType()
    aType.id = 1
    aType.BloodTypeName = "A"

    bType = models.BloodType()
    bType.id = 2
    bType.BloodTypeName = "B"

    abType = models.BloodType()
    abType.id = 3
    abType.BloodTypeName = "AB"

    oType = models.BloodType()
    oType.id = 4
    oType.BloodTypeName = "O"

    superAdmin = models.User()
    superAdmin.UserId = 1
    superAdmin.FirstName = "Super"
    superAdmin.LastName = "Admin"

    superAdminRole.Users.append(superAdmin)
    superAdminCredential = models.UserCredential()
    superAdminCredential.UserCredentialId = 1
    superAdminCredential.Email = "admin@eshiblood.com"
    superAdminCredential.Password = "admin@eshiblood123"
    superAdminCredential.User = superAdmin

    try:
        db.session.add_all([superAdminRole, adminRole, donorRole, nurseRole,
                            aType, bType, abType, oType, superAdmin, superAdminCredential])
        db.session.commit()
    except Exception:
        pass
