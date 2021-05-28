from eshiBlood import app, db, api
from eshiBlood.forms.forms import LoginForm, SignUpForm
from eshiBlood.models.models import UserCredential, User
from eshiBlood.resources.auth import *
from eshiBlood.resources.appointments import *


api.add_resource(UserLoginResource, "/login")
api.add_resource(UserRegisterResource, "/register")

api.add_resource(AppointmentResource,"/appointment")


if __name__ == "__main__":
    app.run()
