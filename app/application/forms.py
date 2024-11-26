from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, URLField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


class ApplicationForm(FlaskForm):
    """
    A class to represents the input fields for adding a new application

    Fields
    --------------
    name: text
        Name of the application
    team_name: text
       Name of the development team who owns the application
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
    bitbucket = URLField('Bitbucket link', [DataRequired()])
    extra_info = TextAreaField('Extra information', [validators.Length(max=250)])
    production_pods = IntegerField('Number of production pods', [DataRequired()])
    server = SelectField('Server', [DataRequired()], coerce=str)

    def validate_server(self, field):
        if field.data == 'Please Select':
            raise ValidationError('Please select a server')
