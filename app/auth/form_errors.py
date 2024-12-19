from enum import Enum

class RegistrationFormError(Enum):
    EMAIL_EXISTS = 'An account with this email address already exists. Please login'
    PASSWORDS_DO_NOT_MATCH = 'Passwords must match'
    PASSWORD_DOES_NOT_MEET_REQUIREMENTS = 'Password does not meet the requirements'
    INVALID_PASSWORD_LENGTH = 'Password cannot exceed 20 characters'
    INVALID_FIRST_NAME_LENGTH = 'First name cannot exceed 150 characters'
    INVALID_FIRST_NAME_FORMAT = 'First name must only contain alphabetic characters and hyphens. First name cannot start or end with a hyphen'
    INVALID_LAST_NAME_LENGTH = 'Last name cannot exceed 150 characters'
    INVALID_LAST_NAME_FORMAT = 'Last name must only contain alphabetic characters and hyphens. Last name cannot start or end with a hyphen'

class LoginFormErrors(Enum):
    INCORRECT_EMAIL_OR_PASSWORD = 'Incorrect email or password'