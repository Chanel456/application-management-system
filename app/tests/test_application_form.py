from app.application.forms import ApplicationForm

def test_form__passes(app):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': 'Example App', 'team_name': 'Team One', 'team_email': 'teamone@gmail.com', 'url': 'https://exampleappone.com', 'swagger_link': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2})
            assert form.validate() == True

def test_form_missing_required_data_validation_fails(app, application_form):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': None, 'team_name': None , 'team_email': None , 'url': 'https://exampleappone.com', 'swagger_link': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2})
            assert form.validate() == False


def test_employee_form_invalid_input_validation_fails(app, application_form):
    with app.app_context():
        with app.test_request_context():
            form = ApplicationForm(data = {'name': '1234567', 'team_name': '431689708', 'team_email': 'teamone@gmail.com', 'url': 'https://exampleappone.com', 'swagger_link': 'https://exampleappone.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone', 'extra_info': None, 'production_pods': 2})
            assert form.validate() == False
            assert form.errors.get('name')[0] == 'Application name must only contain alphabetic characters and hyphens'
            assert form.errors.get('team_name')[0] == 'Team name must only contain alphabetic characters hyphens'