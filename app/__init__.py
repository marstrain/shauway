#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import   Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config

mail = Mail()


app = Flask(__name__)
app.config.from_object(__name__)
from app import views

