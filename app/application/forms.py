import validators as valid_package
from flask import g

from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, URLField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange

from app.models.application import Application
from app.shared.shared import FormType


class ApplicationForm(FlaskForm):
    """
    A class to represents the input fields for adding a new application

    Fields
    --------------
    name: text
        Name of the application
    team_name: text
       Name of the development team who owns the application
    team_email : email
        Email address of development team who owns the application
    url: url
        Url for the application
    swagger: url
        Swagger link for the application if there is any
    bitbucket: url
        Url of the bitbucket repo for the application
    extra_info: text
        Any extra information other should know about the application
    production_pods: number
        The number of pods this application has up in production
    server: dropdown
        The server the application is deployed on
    """

    name = StringField('Application Name', [DataRequired(), validators.Length(min=2, max=150, message='Name must be between 2 and 150 characters cannot exceed 150 characters'), validators.Regexp('^[a-zA-Z- ]+$', message='Application name must only contain alphabetic characters and hyphens')])
    team_name = StringField('Development team', [DataRequired(), validators.Length(min=2, max=50, message='Development team name must be between 2 and 150 characters'), validators.Regexp('^[a-zA-Z- ]+$', message='Team name must only contain alphabetic characters hyphens')])
    team_email = EmailField('Development team email', [DataRequired(), validators.length(max=150, message='Development team email cannot exceed 150 characters')])
    url = URLField('Application URL', [DataRequired(), validators.Length(max=200, message='URL cannot exceed 150 characters')])
    swagger = URLField('Swagger URL', [validators.Optional(), validators.Length(max=200, message='Swagger URL cannot exceed 200 characters')])
    bitbucket = URLField('Bitbucket URL', [DataRequired(), validators.Length(max=200, message='Bitbucket URL cannot exceed 200 characters')])
    extra_info = TextAreaField('Extra information', [validators.Length(max=1000, message='Extra Information cannot exceed 1000 characters')])
    production_pods = IntegerField('Number of production pods', [NumberRange(min=0)])
    server = SelectField('Server', [DataRequired()], coerce=str)

    def validate_name(self, field):
        """Checks if there is an application with the same name already in the Application table"""
        retrieved_application = Application.find_application_by_name(field.data)

        if g.form_type == FormType.UPDATE.value and retrieved_application and  retrieved_application.id != g.application_id:
            raise ValidationError('An application with this name already exists')
        elif g.form_type == FormType.CREATE.value and retrieved_application:
            raise ValidationError('An application with this name already exists')


    def validate_team_email(self, field):
        """Checks if the email address is valid using the validators package"""
        if not valid_package.email(field.data):
            raise ValidationError('Please enter a valid email')

    def validate_server(self, field):
        """Ensures the users has selected a server and is not submitted the placeholder field"""
        if field.data == 'Please Select':
            raise ValidationError('Please select a server')

    def validate_bitbucket(self, field):
        """Validates if bitbucket url starts with https://bitbucket.org and does not contradict to an existing one in the Application table"""

        retrieved_application = Application.find_application_by_bitbucket(field.data)

        if g.form_type == FormType.UPDATE.value and retrieved_application and retrieved_application.id != g.application_id:
            raise ValidationError('An application with this bitbucket already exists')
        elif g.form_type == FormType.CREATE.value and retrieved_application:
            raise ValidationError('An application with this bitbucket already exists')

        if not field.data.startswith('https://bitbucket.org') or not valid_package.url(field.data):
            raise ValidationError('Please enter a valid bitbucket url. Url should start with https://bitbucket.org')

    def validate_swagger(self, field):
        """Checks if a valid url was entered for swagger and does not contradict to an existing one in the Application table"""

        retrieved_application = Application.find_application_by_swagger(field.data)

        if g.form_type == FormType.UPDATE.value and retrieved_application and retrieved_application.id != g.application_id:
            raise ValidationError('An application with this swagger already exists')
        elif g.form_type == FormType.CREATE.value and retrieved_application:
            raise ValidationError('An application with this swagger already exists')

        if not valid_package.url(field.data):
            raise ValidationError('Please enter a valid URL')

    def validate_url(self, field):
        """Checks if a valid url was entered for the application url and does not contradict to an existing one in the Application table"""
        retrieved_application = Application.find_application_by_url(field.data)

        if g.form_type == FormType.UPDATE.value and retrieved_application and retrieved_application.id != g.application_id:
            raise ValidationError('An application with this URL already exists')
        elif g.form_type == FormType.CREATE.value and retrieved_application:
            raise ValidationError('An application with this URL already exists')

        if not valid_package.url(field.data):
            raise ValidationError('Please enter a valid URL')

    def validate_production_pods(self, field):
        """Checks if a valid integer greater than or equal to 0 was entered for the production_pods field"""
        try:
            isinstance(field.data, int) and field.data >= 0
        except (TypeError, ValueError):
            raise ValidationError('Please enter a valid integer greater than 0.')
