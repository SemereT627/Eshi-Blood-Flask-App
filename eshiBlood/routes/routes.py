from flask import render_template, url_for, flash, redirect
from eshiBlood import app, db
from eshiBlood.forms.forms import LoginForm, SignUpForm
from eshiBlood.models.models import UserCredential, User

@app.route('/register')
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        
    return render_template("auth/register.html", form=form)

@app.route('/')
@app.route('/login')
def login():

    return render_template("auth/login.html")

@app.route('/admin/index')
def admin():
    return render_template("admin/index.html")

@app.route('/user/index')
def user():
    return render_template("user/index.html")