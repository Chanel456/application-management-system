from flask import session
from flask_login import current_user

from app.auth.routes import find_user_by_email
from app.models.user import User


def test_registration(client, app):
    client.post('/register', data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test', 'password': '#Password12345', 'confirm_password': '#Password12345'})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == 'test@gmail.com'

def test_login(client):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test', 'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    response = client.post('/login', data ={'email': 'test@gmail.com', 'password': '#Password12345'})
    assert response.headers['Location'] == '/dashboard'

    with client:
        client.get('/dashboard')
        assert session['_user_id'] == '1'
        assert current_user.email == 'test@gmail.com'


def test_logout(client):
    client.post('/register',
                data={'account_type': 'regular', 'email': 'test@gmail.com', 'first_name': 'Test', 'password': '#Password12345',
                      'confirm_password': '#Password12345'})
    client.post('/login', data={'email': 'test@gmail.com', 'password': '#Password12345'})
    response = client.get('/logout')
    assert response.headers['Location'] == '/login'

def test_find_user_by_email_found(init_user_table):
    user = find_user_by_email('test.user1@gmail.com')
    assert user is not None
    assert user.first_name == 'testuser1'

def test_find_user_by_email_not_found(init_user_table):
    user = find_user_by_email('does-not-exist@gmail.com')
    assert user is None