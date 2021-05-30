from eshiBlood.models import models
from eshiBlood import db
from eshiBlood.models.enums import Role


def initialize():
    # database initialize
    # role,
    adminRole = models.UserRole()
    adminRole.UserRoleId = 1
    adminRole.RoleName = Role.Admin

    donorRole = models.UserRole()
    donorRole.UserRoleId = 2
    donorRole.RoleName = Role.Donor

    nurseRole = models.UserRole()
    nurseRole.UserRoleId = 3
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

    try:
        db.session.add_all([adminRole, donorRole, nurseRole,
                            aType, bType, abType, oType])
        db.session.commit()
    except Exception:
        pass

