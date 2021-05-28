import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_restplus import Api
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
api = Api(app,version='1.0',title='Eshi Blood API')

from eshiBlood.utils.security import authenticate,identity
jwt = JWT(app,authenticate,identity)

from eshiBlood.models import models
from eshiBlood.routes import routes
