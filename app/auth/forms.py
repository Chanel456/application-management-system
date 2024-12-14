import validators as valid_package

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import validators, StringField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, ValidationError

from app.models.user import User

class RegistrationForm(FlaskForm):
    """
    A class to represents the input fields for registering a new user for this application

    Fields
    -----------
    account_type: radio
        The type of account to be created. Admin or regular
    email: email
        The email address of the user signing up for the account
    first_name: text
        The first name of the person signing up for the account
    last_name: text
        The last name of the person signing up for the account
    password: password
        The password used to sign to the created account
    confirm_password: password
        Confirm the password used to sign to the account
    """
    account_type = RadioField('Select Account Type:',[DataRequired()], choices=[('admin','Admin'),('regular','Regular')])
    email = EmailField('Email', [DataRequired()])
    first_name = StringField('First Name', [DataRequired(), validators.Length(min=2, max=15), validators.Regexp('^[A-Za-z-]+$', message='First name must only contain alphabetic characters and hyphens. First name cannot start or end with a hyphen')])
    last_name = StringField('Last Name', [DataRequired(), validators.Length(min=2, max=15), validators.Regexp('^[A-Za-z-]+$', message='Last name must only contain alphabetic characters and hyphens. Last name cannot start or end with a hyphen')])
    password = PasswordField('Password', [DataRequired(), validators.Regexp('^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{7,}$', message='Password must contain at least 1 uppercase letter, 1 number,  1 special character [!@#$%^&*()_+] and be at least 7 characters long'), validators.Length(min=7, max=20), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), validators.Regexp('^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{7,}$', message='Password must contain at least 1 uppercase letter, 1 number,  1 special character [!@#$%^&*()_+] and be at least 7 characters long'), validators.EqualTo('password', message='Passwords must match')])

    def validate_email(self, field):
        """Checks if the email address is valid using the validators package"""
        if not valid_package.email(field.data):
            raise ValidationError('Please enter a valid email')

class LoginForm(FlaskForm):
    """
    A class to represents the input fields for signing in to the application

    Fields
    -------------
    email: email
        The email address for the account
    password: password
        The password linked to the email address used to sign in to the account
    """
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate_password(self, field):
        """checks if the password entered in correct for the corresponding email address in the database"""
        user = User.query.filter_by(email=self.email.data).first()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError('Incorrect email or password')