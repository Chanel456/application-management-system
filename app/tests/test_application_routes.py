from flask_login import current_user

from app.application import application
from app.application.routes import find_application_by_id, find_application_by_name, find_application_by_url, \
    find_application_by_bitbucket
from app.models.application import Application

def test_create(client, app, auth, init_server_table):
    auth.register('Test', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    with client:
        with app.app_context():
            response = client.post('/application/create',
                                   data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                                         'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger',
                                         'bitbucket': 'https://bitbucket.com/repo/exampleappone', 'extra_info': '',
                                         'production_pods': 3, 'server': 'exampleserver1'})
            assert response.status_code == 200
            application = Application.query.filter_by(name='Example App').first()
            assert application is not None


def test_update(client, app, auth, init_server_table):
    auth.register('Test', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/application/create',
                    data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                          'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger',
                          'bitbucket': 'https://bitbucket.com/repo/exampleappone', 'extra_info': '',
                          'production_pods': 3, 'server': 'exampleserver1'})

    with app.app_context():
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None
        assert application.team_email == 'team@gmail.com'

    with client:
        response = client.post(f'/application/update?application_id={application.id}',
                            data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'newteamemail@gmail.com',
                                  'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger',
                                  'bitbucket': 'https://bitbucket.com/repo/exampleappone', 'extra_info': '',
                                  'production_pods': 3, 'server': 'exampleserver1'})
        assert response.status_code == 200
        application = Application.query.filter_by(id=application.id).first()
        assert application.team_email == 'newteamemail@gmail.com'



def test_delete_admin_passes(client, app, auth, init_server_table):
    auth.register('Test', 'test@gmail.com', '#Password12345', '#Password12345', 'admin')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/application/create',
                data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                          'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger',
                          'bitbucket': 'https://bitbucket.com/repo/exampleappone', 'extra_info': '',
                          'production_pods': 3, 'server': 'exampleserver1'})


    with app.app_context():
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

    with client:
        client.get(f'/application/delete?application_id={application.id}')
        # assert current_user.is_admin == True # to fix i need to introduce sessions
        application = Application.query.filter_by(name='Example App').first()
        assert application is None


def test_delete_regular_fails(client, app, auth, init_server_table):
    auth.register('Test', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')

    client.post('/application/create',
                data={'name': 'Example App', 'team_name': 'Team', 'team_email': 'team@gmail.com',
                          'url': 'https://exampleappone.com', 'swagger': 'https://exampleappone.com/swagger',
                          'bitbucket': 'https://bitbucket.com/repo/exampleappone', 'extra_info': '',
                          'production_pods': 3, 'server': 'exampleserver1'})


    with app.app_context():
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

    with client:
        client.get(f'/application/delete?application_id={application.id}')
        assert current_user.is_admin == False
        application = Application.query.filter_by(name='Example App').first()
        assert application is not None

def test_find_app_by_name_found(init_application_table):
    application = find_application_by_name('Example App One')
    assert application is not None
    assert application.name == 'Example App One'
    assert application.url == 'https://exampleappone.com'

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

def test_find_app_by_url_found(init_application_table):
    application = find_application_by_url('https://exampleappone.com')
    assert application is not None
    assert application.name == 'Example App One'
    assert application.production_pods == 1

def test_find_app_by_url_not_found(init_application_table):
    application = find_application_by_url('https://urlnotfound.com')
    assert application is None

def test_find_app_by_bitbucket_found(init_application_table):
    application = find_application_by_bitbucket('https://bitbucket.com/repos/exampleapptwo')
    assert application is not None
    assert application.name == 'Example App Two'
    assert application.production_pods == 1

def test_find_app_by_bitbucket_not_found(init_application_table):
    application = find_application_by_bitbucket('https:/bitbucketnotfound.com')
    assert application is None