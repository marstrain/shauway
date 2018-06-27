#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import   Flask,render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection  = 'strong'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    db.init_app(app)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u'hello '

    return app
