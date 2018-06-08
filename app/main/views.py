from flask import render_template
from datetime import datetime

from . import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/post')
def post():
    return render_template('post.html')

@main.route('/logout')
def logout():
    return render_template('logout.html')
