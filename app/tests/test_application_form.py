import pytest
from wtforms.validators import ValidationError

from app.application.forms import ApplicationForm
from app.models.server import Server

def test_application_form_passes(app, init_server_table):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': 'Example App', 'team_name': 'Team One', 'team_email': 'teamone@gmail.com', 'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2, 'server': 'exampleserver1'})
            form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]
            assert form.validate() == True

def test_application_form_missing_required_data_validation_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': None, 'team_name': None , 'team_email': None , 'url': 'https://exampleappone.com', 'swagger_link': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2, 'server': 'exampleserver1'})
            form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]
            assert form.validate() == False


def test_employee_form_invalid_input_validation_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': '1234567', 'team_name': '431689708', 'team_email': 'teamone@gmail.com', 'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2, 'server': 'exampleserver1'})
            form.server.choices = [(s.name, s.name) for s in Server.query.with_entities(Server.name)]
            assert form.validate() == False
            assert form.errors.get('name')[0] == 'Application name must only contain alphabetic characters and hyphens'
            assert form.errors.get('team_name')[0] == 'Team name must only contain alphabetic characters hyphens'

def test_email_validator_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.team_email.data = 'teamone@gmail.com'
            form.validate_team_email(form.team_email)
            assert form.team_email.errors.__len__() == 0

def test_email_validator_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.team_email.data = 'teaminvalidemail@gmail'
            with pytest.raises(ValidationError):
                form.validate_team_email(form.team_email)

def test_validate_server_passes(app, init_server_table):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.server.data = 'exampleserver1'
            form.validate_server(form.server)
            assert form.server.errors.__len__() == 0

def test_validate_server_fails(app, init_server_table):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.server.data = 'Please Select'
            with pytest.raises(ValidationError):
                form.validate_server(form.server)

def test_validate_bitbucket_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.bitbucket.data = 'https://bitbucket.com/repo/exampleapp'
            form.validate_bitbucket(form.bitbucket)
            assert form.bitbucket.errors.__len__() == 0

def test_validate_bitbucket_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.bitbucket.data = 'https://bitbucketInv$id/repos/exampleapp'
            with pytest.raises(ValidationError):
                form.validate_bitbucket(form.bitbucket)

def test_validate_swagger_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.swagger.data = 'https://exampleapp.com/api/ui'
            form.validate_swagger(form.swagger)
            assert form.swagger.errors.__len__() == 0

def test_validate_swagger_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.swagger.data = 'hts://exampleapp/swagger/'
            with pytest.raises(ValidationError):
                form.validate_swagger(form.swagger)

def test_validate_url_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.url.data = 'https://exampleapp.com'
            form.validate_url(form.url)
            assert form.url.errors.__len__() == 0

def test_validate_url_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm()
            form.url.data = 'hts://exampleapp'
            with pytest.raises(ValidationError):
                form.validate_url(form.url)