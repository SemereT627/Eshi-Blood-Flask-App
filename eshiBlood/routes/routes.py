from eshiBlood import app, db, api
from eshiBlood.forms.forms import LoginForm, SignUpForm
from eshiBlood.models.models import UserCredential, User
from eshiBlood.resources.auth import *


api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run()
