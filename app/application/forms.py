from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, URLField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class ApplicationForm(FlaskForm):
    name = StringField('Application Name', [DataRequired(), validators.Length(min=2, max=70), validators.Regexp('^[a-zA-Z- ]+$', message='Application name must only contain alphabetic characters and hyphens')])
    team_name = StringField('Development team', [DataRequired(), validators.Length(min=3, max=30), validators.Regexp('^[a-zA-Z- ]+$', message='Team name must only contain alphabetic characters hyphens')])
    team_email = EmailField('Development team email', [DataRequired()])
    url = URLField('Application URL', [DataRequired()])
    swagger = URLField('Application swagger')
    bitbucket = URLField('Bitbucket link', [DataRequired()])
    extra_info = TextAreaField('Extra information', [validators.Length(max=250)])
    production_pods = IntegerField('Number of production pods', [DataRequired()])