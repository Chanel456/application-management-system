from flask import g
from flask_wtf import FlaskForm

from wtforms import validators, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app.models.server import Server
from app.shared.shared import FormType


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

    name = StringField('Server Name', [DataRequired(), validators.Length(max=50, message="Server name cannot exceed 50 characters"), validators.Regexp('^[a-zA-Z0-9-]{1,50}$', message='Server name can only contain letters, numbers and hyphens with no spaces i.e: ab-1234')])
    cpu = IntegerField('CPU (GHz)', [NumberRange(min=1)])
    memory = IntegerField('Memory (GiB)', [NumberRange(min=1)])
    location = StringField('Location', [DataRequired(), validators.Regexp('^[a-zA-Z\s]+$', message='Location can only contain alphabetic characters'), validators.Length(max=50, message='Location cannot exceed 50 characters')])

    def validate_cpu(self, field):
        """Checks if CPU is valid"""
        check_if_valid_integer_and_greater_then_zero(field.data)


    def validate_memory(self, field):
        """Checks if Memory is valid"""
        check_if_valid_integer_and_greater_then_zero(field.data)


    def validate_name(self, field):
        """Checks if there is a server with the same name already in the Server table"""
        retrieved_server = Server.find_server_by_name(field.data)

        if g.form_type == FormType.UPDATE.value and retrieved_server and retrieved_server.id != g.server_id:
            raise ValidationError('A server with this name already exists')
        elif g.form_type == FormType.CREATE.value and retrieved_server:
            raise ValidationError('An server with this name already exists')


def check_if_valid_integer_and_greater_then_zero(number):
    """Checks if an integer was entered"""
    try:
        isinstance(number, int) and number >= 1
    except (TypeError, ValueError):
        raise ValidationError('Please enter a valid integer greater than 1.')