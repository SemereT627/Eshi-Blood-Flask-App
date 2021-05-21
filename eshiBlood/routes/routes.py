from flask import render_template, url_for, flash, redirect
from eshiBlood import app


@app.route('/register')
def register():
    return render_template("auth/register.html")

@app.route('/login')
def login():
    return render_template("auth/login.html")

@app.route('/admin/index')
def admin():
    return render_template("admin/index.html")

@app.route('/user/index')
def user():
    return render_template("user/index.html")