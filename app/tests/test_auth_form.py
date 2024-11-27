import pytest
from wtforms.validators import ValidationError

from app.auth.forms import LoginForm, RegistrationForm


def test_password_validator_passes(init_user_table, app):
    with app.app_context():
        with app.test_request_context():
            form = LoginForm(data={'email': 'test.user1@gmail.com', 'password': '#Password12345'})
            form.validate_password(form.password)
            assert form.password.errors.__len__() == 0

def test_password_validator_fails(init_user_table, app):
    with app.app_context():
        with app.test_request_context():
            form = LoginForm(data = {'email': 'test.user1@gmail.com', 'password': '#Incorr£TPa$$word'})
            with pytest.raises(ValidationError):
                form.validate_password(form.password)

def test_email_validator_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = RegistrationForm(data ={'account_type': 'regular', 'email': 'test.user1@gmail.com', 'first_name': 'Hello', 'password': '#Password1234', 'confirm_password': '#Password1234'} )
            form.validate_email(form.email)
            assert form.email.errors.__len__() == 0

def test_email_validator_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = RegistrationForm(data ={'account_type': 'regular', 'email': 'test.user1@gmail', 'first_name': 'Hello', 'password': '#Password1234', 'confirm_password': '#Password1234'} )
            with pytest.raises(ValidationError):
                form.validate_email(form.email)

def test_registration_form_validation_passes(app):
    with app.app_context():
        with app.test_request_context():
            form = RegistrationForm(data={'account_type': 'regular', 'email': 'test.user1@gmail.com', 'first_name': 'Hello', 'password': '#Password1234', 'confirm_password': '#Password1234'})
            assert form.validate() == True

def test_registration_form_validation_fails(app):
    with app.app_context():
        with app.test_request_context():
            form = RegistrationForm( data={'account_type': 'regular', 'email': 'test.user1@', 'first_name': 'Hello', 'password': '#Password34', 'confirm_password': '#Password14'})
            assert form.validate() == False