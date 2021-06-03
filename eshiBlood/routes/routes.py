from eshiBlood import app, db
from eshiBlood.forms.forms import LoginForm, SignUpForm
from eshiBlood.models.models import UserCredential, User
from eshiBlood.resources.auth import *
from flask_restplus import Api

api = Api(app,version='1.0',title='Eshi Blood API')

from eshiBlood.resources.auth.admin.auth_admin import admin_auth_ns
from eshiBlood.resources.auth.nurse.auth_nurse import nurse_auth_ns
from eshiBlood.resources.auth.donor.auth_donor import donor_auth_ns
from eshiBlood.resources.appointments.appointments import appointment_ns
from eshiBlood.resources.events.events import event_ns
from eshiBlood.resources.requests.requests import request_ns
from eshiBlood.resources.donation_centers.donation_centers import donation_center_ns


api.add_namespace(admin_auth_ns)
api.add_namespace(donor_auth_ns)
api.add_namespace(nurse_auth_ns)
api.add_namespace(appointment_ns)
api.add_namespace(event_ns)
api.add_namespace(request_ns)
api.add_namespace(donation_center_ns)
