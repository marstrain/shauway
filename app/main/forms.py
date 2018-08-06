# -*- coding :utf8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import  TextAreaField, SubmitField, TextField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

class PostForm(Form):
    title = TextField('enter a  title', validators = [DataRequired()])
    body = TextAreaField("What's in your mind", validators = [DataRequired()])
    category = SelectField(u'category', choices = [('1','life'), ('2','tech'),('3','news')])
    submit = SubmitField("submit")

