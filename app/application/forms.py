from flask_wtf import FlaskForm
from wtforms import validators, StringField, EmailField, SelectField, URLField
from wtforms.validators import DataRequired,  ValidationError

class ApplicationForm(FlaskForm):
    name = StringField('Application Name', [DataRequired(), validators.Length(min=2, max=70), validators.Regexp('^[a-zA-Z\- ]+$', message='Application name must only contain alphabetic characters and hyphens')])
    team_name = StringField('Development team', [DataRequired(), validators.Length(min=3, max=30), validators.Regexp('^[a-zA-Z\- ]+$', message='Team name must only contain alphabetic characters hyphens')])
    team_email = EmailField('Development team email', [DataRequired()])
    url = URLField('Application URL', [DataRequired()])
    swagger_link = URLField('Application swagger link')
    status = SelectField('Application Status',[DataRequired()], choices=[('Please Select','Please Select'), ('Up', 'Up'), ('Down', 'Down'), ('Decommissioned', 'Decommissioned')])

    def validate_status(self, field):
        if field.data == 'Please Select':
            raise ValidationError('Please select an application status')