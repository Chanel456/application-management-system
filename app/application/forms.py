import validators as valid_package

from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, URLField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange


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

    name = StringField('Application Name', [DataRequired(), validators.Length(min=2, max=70), validators.Regexp('^[a-zA-Z- ]+$', message='Application name must only contain alphabetic characters and hyphens')])
    team_name = StringField('Development team', [DataRequired(), validators.Length(min=3, max=30), validators.Regexp('^[a-zA-Z- ]+$', message='Team name must only contain alphabetic characters hyphens')])
    team_email = EmailField('Development team email', [DataRequired()])
    url = URLField('Application URL', [DataRequired()])
    swagger = URLField('Application swagger')
    bitbucket = URLField('Bitbucket', [DataRequired()])
    extra_info = TextAreaField('Extra information', [validators.Length(max=250)])
    production_pods = IntegerField('Number of production pods', [DataRequired(), NumberRange(min=0)])
    server = SelectField('Server', [DataRequired()], coerce=str)

    def validate_team_email(self, field):
        """Checks if the email address is valid using the validators package"""
        if not valid_package.email(field.data):
            raise ValidationError('Please enter a valid email')

    def validate_server(self, field):
        """Ensures the users has selected a server and is not submitted the placeholder field"""
        if field.data == 'Please Select':
            raise ValidationError('Please select a server')

    def validate_bitbucket(self, field):
        """Validates if bitbucket url starts with https://bitbucket.com"""
        if not field.data.startswith('https://bitbucket.com') or not valid_package.url(field.data):
            raise ValidationError('Please enter a valid bitbucket url. Url should start with https://bitbucket.com')

    def validate_swagger(self, field):
        """Checks if a valid url was entered for swagger"""
        if not valid_package.url(field.data):
            raise ValidationError('Please enter a valid url')

    def validate_url(self, field):
        """Checks if a valid url was entered for the application url"""
        if not valid_package.url(field.data):
            raise ValidationError('Please enter a valid url')
