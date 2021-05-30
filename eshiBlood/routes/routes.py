from eshiBlood import app, db
from eshiBlood.forms.forms import LoginForm, SignUpForm
from eshiBlood.models.models import UserCredential, User
from eshiBlood.resources.auth import *
from eshiBlood.resources.appointments import *
from flask_restplus import Api

api = Api(app,version='1.0',title='Eshi Blood API')

from eshiBlood.resources.auth.auth import auth_ns
from eshiBlood.resources.appointments.appointments import appointment_ns
from eshiBlood.resources.events.events import event_ns
from eshiBlood.resources.requests.requests import request_ns
from eshiBlood.resources.donation_centers.donation_centers import donation_center_ns
from eshiBlood.resources.auth.auth_admin import auth_admin

api.add_namespace(auth_ns)
api.add_namespace(appointment_ns)
api.add_namespace(event_ns)
api.add_namespace(request_ns)
api.add_namespace(donation_center_ns)
api.add_namespace(auth_admin)