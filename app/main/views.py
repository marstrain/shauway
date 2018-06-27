from flask import render_template,  redirect, url_for, session,g
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_login import  login_required
from forms import PostForm

from . import main
from .. import db
from ..models import User

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html',name=session.get('name'))

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')



@main.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm
    if form.validate_on_submit():
        post = Post()
    return render_template('post.html')







