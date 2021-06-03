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

from eshiBlood.utils.initializer import initialize
# initialize()
