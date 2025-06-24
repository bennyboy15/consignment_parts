from flask_wtf import FlaskForm
from wtforms import FieldList, FloatField, FormField, IntegerField, SelectField, StringField, PasswordField, SubmitField
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

# Subform for individual OrderItem
class OrderItemForm(FlaskForm):
    part = SelectField('Part', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])

# Main Order creation form
class OrderForm(FlaskForm):
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    items = FieldList(FormField(OrderItemForm), min_entries=1)
    submit = SubmitField('Create Order')