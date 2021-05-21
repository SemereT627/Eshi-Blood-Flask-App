from flask_wtf import FlaskForm
from wtforms import validators
from eshiBlood.models.enums import *
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=4, max=10)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    userName = StringField("Username", validators=[DataRequired(), Length(
        min=4, max=10, message="Username too long")])

    firstName = StringField("First Name", validators=[
                            DataRequired(), Length(min=3, message="First name is too short")])

    lastName = StringField("First Name", validators=[
                           DataRequired(), Length(min=3, message="Last name is too short")])

    phone = StringField(
        "Your Phone +251-", validators=[DataRequired(), Length(min=9, message="too short")])

    emergencyContactName = StringField("Emergency Contact Name", validators=[
                                       DataRequired(), Length(min=3, message="Name is too short")])

    emergencyContactPhone = StringField("Emergency Contact Phone +251-", validators=[
                                        DataRequired(), Length(min=9, max=10, message="too short")])

    addressLine = StringField("Address Line", validators=[DataRequired()])

    postCode = StringField("Post Code", validators=[DataRequired()])

    zone = StringField("Zone", validators=[DataRequired()])

    state = StringField("State", validators=[DataRequired()])

    city = StringField("City", validators=[DataRequired()])

    gender = SelectField("Gender", choices=[Gender.Male, Gender.Female])

    bloodType = SelectField("Blood Type", choices=["O", "A", "AB", "B"])

    dob = StringField("Date of birthday", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[
                            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
