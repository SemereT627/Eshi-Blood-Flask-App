
from eshiBlood.models.enums import *
from wtforms import Form, BooleanField, StringField, PasswordField, validators,SelectField
import sys
sys.path.append("../models")


class LoginForm(Form):
    UserName = StringField("UserName")
    Password = PasswordField("Password")


class SignUpForm(Form):
    userName = StringField("UserName", validators=[
                           validators.Length(min=4, max=10, message="User Name too long")])
                           
    firstName = StringField("First Name", validators=[validators.InputRequired(
        "Required"), validators.Length(min=3, message="First Name is too short")])

    lastName = StringField("First Name", validators=[
                           validators.InputRequired("Required")])

    phone = StringField("Your Phone +251-", validators=[validators.InputRequired(
        "Required"), validators.Length(min=9, message="too short")])

    emergencyContactName = StringField("Emergency Contact Name", validators=[validators.InputRequired(
        "Required"), validators.Length(min=3, message="Name is too short")])

    emergencyContactPhone = StringField("Emergency Contact Phone +251-", validators=[validators.InputRequired(
        "Required"), validators.Length(min=9, max=10, message="too short")])

    addressLine = StringField("Address Line", validators=[validators.InputRequired(
        "Required")])

    postCode = StringField("Post Code", validators=[validators.InputRequired(
        "Required")])

    zone = StringField("Zone", validators=[validators.InputRequired(
        "Required")])

    state = StringField("State", validators=[validators.InputRequired(
        "Required")])

    city = StringField("City", validators=[validators.InputRequired(
        "Required")])

    gender = SelectField("Gender",choices=[Gender.Male,Gender.Female])

    bloodType = SelectField("Blood Type",choices=["O","A","AB","B"])

    dob = StringField("Date of birthday", validators=[validators.InputRequired(
        "Required")])
    
    email = StringField("Email", validators=[
                        validators.Email("invalid email")])
    password = PasswordField('New Password', validators=[
                             validators.InputRequired()])
    confirm = PasswordField('Repeat Password', validators=[ validators.EqualTo(
        'password', message='Passwords must match')])
