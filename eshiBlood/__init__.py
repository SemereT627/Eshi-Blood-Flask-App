import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, model
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_jwt import JWT
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)


from eshiBlood.utils.security import authenticate,identity
jwt = JWT(app,authenticate,identity)

from eshiBlood.models import models
from eshiBlood.routes.routes import api
from eshiBlood.models.enums import *


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
    db.session.add_all([adminRole,donorRole,nurseRole,aType,bType,abType,oType])
    db.session.commit()
except Exception:
    pass