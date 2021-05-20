from eshiBlood.templates.forms import *
from flask import Flask
from flask.templating import render_template
import jinja2

app = Flask(__name__)


@app.route('/')
def hello():
    form = SignUpForm()
    return render_template("auth/register.html",form=form)