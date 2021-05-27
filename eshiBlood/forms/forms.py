from flask_wtf import FlaskForm
from wtforms import validators
from eshiBlood.models.enums import *
from wtforms import StringField, RadioField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=4, max=10)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    # Start::Personal Information
    firstName = StringField("First Name", validators=[
                            DataRequired(), Length(min=4, message="First name is too short")])
    lastName = StringField("Last Name", validators=[
                           DataRequired(), Length(min=4, message="Last name is too short")])
    gender = SelectField("Gender", choices=[(1, "Male"), (2, "Female")])
    dateOfBirth = StringField("Date of birth", validators=[DataRequired()])
    # End::Personal Information

    # Start::Address
    city = StringField("City", validators=[DataRequired()])  # TBD
    state = SelectField("State", choices=[
                        (1, "Addis Ababa"), (2, "Tigray"), (3, "Afar"), (4, "Amhara"), (5, "Oromia"), (6, "Benishangul"), (7, "Harar"), (8, "Somali"), (9, "South Nations"), (10, "Sidama State"), (11, "Dire Dawa")])
    zone = StringField("Zone", validators=[DataRequired()])
    woreda = StringField("Woreda", validators=[DataRequired()])
    kebele = StringField("Kebele", validators=[DataRequired()])
    postCode = StringField("Post Code", validators=[DataRequired()])
    # End::Address

    # Start::Emergency Contact
    emergencyContactName = StringField("Emergency Contact Name", validators=[
        DataRequired(), Length(min=3, message="Name is too short")])

    emergencyContactPhoneNumber = StringField("Emergency Contact Phone Number", validators=[
        DataRequired(), Length(min=9, max=10, message="too short")])
    # End::Emergency Contact


    # Start::User Credentials
    userName = StringField("Username", validators=[DataRequired(), Length(
        min=4, max=10, message="Username too long")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password')])
    phoneNumber = StringField(
        "Your phone number", validators=[DataRequired(), Length(min=9, message="too short")])
    # End::User Credentials

    submit = SubmitField('Sign up')
