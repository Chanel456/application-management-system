import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.application import Application
from app.models.server import Server
from app.models.user import User
from config.test_config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture
def client(app):
    app.config['WTF_CSRF_ENABLED'] = False
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, first_name, email, password, confirm_password, account_type):
        # is_admin = True if is_admin == 'admin' else False
        return self._client.post(
            '/auth/register',
            data={'first_name': first_name, 'email': email, 'password': password, 'confirm_password': confirm_password, 'account_type': account_type }
        )

    def login(self, email, password):
        return self._client.post(
           '/auth/login',
            data={'email': email, 'password': password},
            follow_redirects = True
        )

    def logout(self):
        return  self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def init_user_table(app):
    with app.app_context():
        user1 = User(first_name='testuser1', email='test.user1@gmail.com',
                     password=generate_password_hash('#Password12345', method='scrypt'), is_admin=True)
        user2 = User(first_name='testuser2', email='test.user2@gmail.com',
                     password=generate_password_hash('#Password5678', method='scrypt'), is_admin=True)
        user3 = User(first_name='testuser3', email='test.user3@gmail.com',
                     password=generate_password_hash('#Password1357', method='scrypt'), is_admin=True)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        yield db

@pytest.fixture
def init_application_table(app):
    with app.app_context():
        application1 = Application(name='App One', team_name='Team One',
                               team_email='team.one@gmail.com', url='https://appone.com',
                               swagger='https://appone.com/swagger/ui',
                               bitbucket='https://bitbucket.com/repos/appone', extra_info=None,
                               production_pods=1, server='ab0001')
        application2 = Application(name='App Two', team_name='Team Two',
                               team_email='team.two@gmail.com', url='https://apptwo.com',
                               swagger=None,
                               bitbucket='https://bitbucket.com/repos/apptwo', extra_info='This is an angular application',
                               production_pods=1, server='ab0002')
        application3 = Application(name='App Three', team_name='Team Three',
                               team_email='team.three@gmail.com', url='https://appthree.com',
                               swagger='https://appthree.com/swagger/ui',
                               bitbucket='https://bitbucket.com/appthree', extra_info=None,
                               production_pods=1, server='ab0003')
        db.session.add(application1)
        db.session.add(application2)
        db.session.add(application3)
        db.session.commit()
        yield db

@pytest.fixture
def init_server_table(app):
    with app.app_context():
        server1 = Server(name='exampleserver1', cpu=123, memory=123, location='Walthamstow')
        server2 = Server(name='exampleserver2', cpu=456, memory=456, location='Harrow')
        server3 = Server(name='exampleserver3', cpu=789, memory=789, location='Surrey')
        db.session.add(server1)
        db.session.add(server2)
        db.session.add(server3)
        db.session.commit()
        yield db