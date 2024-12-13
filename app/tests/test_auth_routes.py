from flask import session
from flask_login import current_user

from app.auth.routes import find_user_by_email
from app.models.user import User


def test_registration(app, auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == 'test@gmail.com'

def test_login(client, auth):
    auth.register('Test', 'Smith','test@gmail.com', '#Password12345', '#Password12345', 'regular')
    response = auth.login('test@gmail.com', '#Password12345')
    assert response.status_code == 200

    with client:
        client.get('/dashboard')
        assert session['_user_id'] == '1'
        assert current_user.email == 'test@gmail.com'


def test_logout(auth):
    auth.register('Test', 'Smith', 'test@gmail.com', '#Password12345', '#Password12345', 'regular')
    auth.login('test@gmail.com', '#Password12345')
    response = auth.logout()
    assert response.headers['Location'] == '/auth/login'

def test_find_user_by_email_found(init_user_table):
    user = find_user_by_email('test.user1@gmail.com')
    assert user is not None
    assert user.first_name == 'Testuser1'
    assert user.last_name == 'Smith'

def test_find_user_by_email_not_found(init_user_table):
    user = find_user_by_email('does-not-exist@gmail.com')
    assert user is None