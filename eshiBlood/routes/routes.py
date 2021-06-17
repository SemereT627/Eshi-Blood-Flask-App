from eshiBlood import app, db
from eshiBlood.models.models import UserCredential, User
from flask_restplus import Api

api = Api(app,version='1.0',title='Eshi Blood API')

# from eshiBlood.resources.auth import *
# from eshiBlood.resources.admin import *
# from eshiBlood.resources.donor import *
# from eshiBlood.resources.nurse import *
from eshiBlood.resources.endpoints.appointment import *
from eshiBlood.resources.endpoints.donationcenter import *
from eshiBlood.resources.endpoints.request import *
from eshiBlood.resources.endpoints.event import event_ns
from eshiBlood.resources.endpoints.auth import *
from eshiBlood.resources.endpoints.user import *

api.add_namespace(admin_auth_ns)
api.add_namespace(donor_auth_ns)
api.add_namespace(auth_ns)
api.add_namespace(superadmin_ns)
api.add_namespace(user_ns)

# api.add_namespace(appointment_admin_ns)
# api.add_namespace(event_admin_ns)
# api.add_namespace(request_admin_ns)
# api.add_namespace(donation_centers_admin_ns)

# api.add_namespace(appointment_donor_ns)
# api.add_namespace(event_donor_ns)
# api.add_namespace(request_donor_ns)
# api.add_namespace(donation_center_donor_ns)


# api.add_namespace(appointment_nurse_ns)
# api.add_namespace(event_nurse_ns)
# api.add_namespace(request_nurse_ns)
# api.add_namespace(donation_center_nurse_ns)


api.add_namespace(appointment_ns)
api.add_namespace(donationCenter_ns)
api.add_namespace(request_ns)
api.add_namespace(event_ns)