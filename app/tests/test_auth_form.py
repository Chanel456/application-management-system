import pytest
from wtforms.validators import ValidationError

from app.auth.forms import LoginForm

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
