from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateTimeField
from wtforms import SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class WeighingForm(FlaskForm):
    weight = FloatField('weight (kg)', validators=[DataRequired()])
    geolocation = StringField('geolocation', validators=[DataRequired()])
    weighing_time = DateTimeField('weighing time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Submit')