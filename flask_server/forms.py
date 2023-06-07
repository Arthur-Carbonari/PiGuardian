from flask import app, current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, PasswordField
from flask_bootstrap import SwitchField
from wtforms.validators import InputRequired, Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class NewProfileForm(FlaskForm):
    name = StringField(validators=[
                        DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Name"})
    
    files = FileField('Image', render_kw={"placeholder": "Upload File", "multiple" : "True", "accept": ".jpg"})

class SwitchThemeForm(FlaskForm):
    
    power_switch = SwitchField('Dark Mode', render_kw = {'onchange' : "sendSwitchValue()", 'id' : 'themeSwitch'})

    def check(self, check):
        self.power_switch.render_kw['checked'] = check
        return self
