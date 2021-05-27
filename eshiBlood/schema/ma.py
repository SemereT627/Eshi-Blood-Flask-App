from flask_restplus import fields
from eshiBlood.models.models import UserCredential, User
from flask_marshmallow import Marshmallow
from eshiBlood.models.models import *

ma = Marshmallow()

class UserCredentialSchema(ma.Schema):
    class Meta:
        fields = ("Email","Password")
        model = UserCredential

class UserSchema(ma.Schema):
    class Meta:
        fields = ("FirstName","LastName","UserName","BirthDate","Gender","MartialStatus","BloodType","Address")
        model = User

        