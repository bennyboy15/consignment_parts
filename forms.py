from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class PartForm(FlaskForm):
    name = StringField('Part Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])