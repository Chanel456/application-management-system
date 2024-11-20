from flask_login import current_user

from app.application.routes import find_application_by_id, find_application_by_name
from app.models.application import Application

def test_create(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    with client:
        with app.app_context():
            response = client.post('/create',
                                   data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                                         'url': 'https://exampleapp.com',
                                         'swagger_link': 'https://exampleapp.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone',
                                         'extra_info': None, 'production_pods': 1})
            assert response.status_code == 200
            assert Application.query.count() == 1
            assert Application.query.first().name == 'Example App'


def test_update(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create',
                data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                      'url': 'https://exampleapp.com',
                      'swagger_link': 'https://exampleapp.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone',
                      'extra_info': None, 'production_pods': 1})

    response = client.post('/update?application_id=1',
                           data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'newteamemail@gmail.com',
                                 'url': 'https://exampleapp.com',
                                 'swagger_link': 'https://exampleapp.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone',
                                 'extra_info': None, 'production_pods': 1})
    with app.app_context():
        assert response.status_code == 200
        assert Application.query.count() == 1
        application = Application.query.filter_by(name='Example App').first()
        assert application.team_email == 'newteamemail@gmail.com'



def test_delete_admin_passes(client, app):
    client.post('/register',
                data={'account_type': 'admin', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create',
                data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                      'url': 'https://exampleapp.com',
                      'swagger_link': 'https://exampleapp.com/swagger/ui', 'bitbucket':'https://bitbucket.com/repos/exampleappone',
                      'extra_info': None, 'production_pods': 1})


    with app.app_context():
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

    with client:
        client.get('/delete?application_id=1')
        # assert current_user.is_admin == True # to fix i need to introduce sessions
        application = Application.query.filter_by(name='Example App').first()
        assert application is None


def test_delete_regular_fails(client, app):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test',
                      'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})

    client.post('/create',
                data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                      'url': 'https://exampleapp.com',
                      'swagger_link': 'https://exampleapp.com/swagger/ui', 'bitbucket': 'https://bitbucket.com/repos/exampleappone',
                      'extra_info': None, 'production_pods': 1})


    with app.app_context():
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

    with client:
        client.get('/delete?employee_id=1')
        assert current_user.is_admin == False
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

def test_find_app_by_name_found(init_application_table):
    employee = find_application_by_name('Example App One')
    assert employee is not None
    assert employee.name == 'Example App One'
    assert employee.url == 'https://exampleappone.com'

def test_find_app_by_name_not_found(init_application_table):
    application = find_application_by_name('Example App Not Found')
    assert application is None

def test_find_app_by_id_found(init_application_table):
    application = find_application_by_id('3')
    assert application is not None
    assert application.name == 'Example App Three'
    assert application.url == 'https://exampleappthree.com'

def test_find_app_by_id_not_found(init_application_table):
    application = find_application_by_id('23456789')
    assert application is None