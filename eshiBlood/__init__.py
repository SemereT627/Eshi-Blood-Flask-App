import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, model
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_jwt import JWT
import click
from sqlalchemy import exc
from flask_cors import CORS
load_dotenv()



app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CORS_HEADERS']="Content-Type"



db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)


from eshiBlood.utils.security import authenticate,identity
jwt = JWT(app,authenticate,identity)

from eshiBlood.models import models
from eshiBlood.routes.routes import api

from eshiBlood.utils.initializer import *

@app.cli.command()
def initdb():
    try:
        try:
            engine = SQLAlchemy.create_engine(self=SQLAlchemy,sa_url="postgresql://postgres:root@localhost:5432",engine_opts={})
            conn = engine.connect()
            conn.execute("commit")
            conn.execute("create database eshiblooda")
            conn.close()
            
        except:
            print("database already created")
        try:
            db.create_all()
        except:
            print("tables already created")
        try:
            db.session.rollback()
            
            initializeBloodTypes()
            initializeRoles()
            initializeSuper()

            # initializeDonors()
            # initializeAppointments()
            # initializeEvents()
            # initializeNurses()
        except:
            db.session.rollback()
            initializeBloodTypes()
            initializeRoles()
            initializeSuper()
            # initializeSuper()
            # initializeDonors()
            # initializeAppointments()
            # initializeEvents()
            # initializeNurses()
        
        
    except:
        print("Exception occured")
    # initializeSuper()
    
    
    

@app.cli.command()
def resetdb():
    try:
        try:
            engine = SQLAlchemy.create_engine(self=SQLAlchemy,sa_url="postgresql://postgres:root@localhost:5432",engine_opts={})
            conn = engine.connect()
            conn.execute("commit")
            conn.execute("drop database eshiblood")
            conn.close()
            print("database deleted")
        except:
            print("database already deleted")
    except:
        print("reset ERR")

