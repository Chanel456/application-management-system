from flask_wtf import FlaskForm

from wtforms import validators, StringField, IntegerField
from wtforms.validators import DataRequired


class ServerForm(FlaskForm):
    """
    A class that represents the input fields for adding a new server

    Fields
    ---------------------
    name: text
        The name of the server
    cpu: number
        The amount of CPU the server has
    memory: number
        The amount of memory the server has
    location: text
        The location of the server
    """

    name = StringField('Server Name', [DataRequired(), validators.Regexp('^[a-z]{2}[0-9]{4}$', message='Name should contain 2 lowercase letters followed by 4 numbers')])
    cpu = IntegerField('CPU (GHz)', [DataRequired()])
    memory = IntegerField('Memory (GiB)', [DataRequired()])
    location = StringField('Location', [DataRequired(), validators.Regexp('^[a-zA-Z\s]+$', message='Location can only contain alphabetic characters')])