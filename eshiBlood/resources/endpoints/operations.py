import flask
from flask_restplus import Resource, Namespace
from eshiBlood.models.models import *
from eshiBlood import db
from eshiBlood.routes.routes import api
from datetime import datetime, timedelta
from eshiBlood.schema.ma import requestSchema, addressSchema
from eshiBlood.utils.role_jwt import *
from eshiBlood.utils.operations import days_between, minutes_between

import datetime

def days_between(d1, d2):
    d1 = datetime.datetime.fromisoformat(d1)
    d2 =datetime.datetime.fromisoformat(d2)
    return abs((d2 - d1).days)
def minutes_between(d1,d2):
    d1 = datetime.datetime.fromisoformat(d1)
    d2 =datetime.datetime.fromisoformat(d2)
    return abs(((d2 - d1).days))



def userCanBookAppointment():
    now = str(datetime.datetime.now())
    token = request.headers.get("token")
    uid = getTokenUserId(token)
    lastAppt = Appointment.query.filter((Appointment.Status=="Active") & (Appointment.User==uid)).order_by(Appointment.UpdatedAt.desc()).limit(3).first()
    if(lastAppt==None):
        return True
    else:
        timeDiff = minutes_between(str(lastAppt.UpdatedAt), now)
        if(timeDiff >= 3):
            print("///////////////////////////********************//////////////////")
            print(f"valid time {timeDiff}  {lastAppt.AppointmentDescription}")
            return True
        else:
            return False
