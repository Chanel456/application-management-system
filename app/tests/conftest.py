import datetime

import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.application.forms import ApplicationForm
from app.models.application import Application
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

    def register(self, first_name, email, password, confirm_password, is_admin):
        return self._client.post(
            '/register',
            data={'first_name': first_name, 'email': email, 'password': password, 'confirm_password': confirm_password, 'is_admin': is_admin }
        )

    def login(self, email, password):
        return self._client.post(
           '/login',
            data={'email': email, 'password': password},
            follow_redirects = True
        )

    def logout(self):
        return  self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def application_form(app):
    with app.app_context():
        return ApplicationForm()

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
        application1 = Application( name='Example App One', owner_id=1, team_name='Team One',
                                   team_email='team.one@gmail.com', url='https://exampleappone.com',
                                   swagger_link='https://exampleappone.com/swagger/ui', bitbucket_link=None,
                                   status='Up', created=datetime.datetime(2024, 11, 14, 10, 36, 43, 846344))
        application2 = Application( name='Example App Two', owner_id=1, team_name='Team Two',
                                   team_email='team.two@gmail.com', url='https://exampleapptwo.com',
                                   swagger_link='https://exampleapptwo.com/swagger/ui', bitbucket_link=None,
                                   status='Down', created=datetime.datetime(2024, 11, 14, 10, 36, 43, 846344))
        application3 = Application( name='Example App Three', owner_id=1, team_name='Team Three',
                                   team_email='team.three@gmail.com', url='https://exampleappthree.com',
                                   swagger_link='https://exampleappthree.com/swagger/ui', bitbucket_link=None,
                                   status='Up', created=datetime.datetime(2024, 11, 14, 10, 36, 43, 846344))
        db.session.add(application1)
        db.session.add(application2)
        db.session.add(application3)
        db.session.commit()
        yield db