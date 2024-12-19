from enum import Enum


class ApplicationFormError(Enum):
    URL_EXISTS = 'An application with this URL already exists'
    INVALID_URL_LENGTH = 'Application URL cannot exceed 150 characters'
    SWAGGER_EXISTS = 'An application with this swagger already exists'
    INVALID_SWAGGER_LENGTH ='Swagger URL cannot exceed 200 characters'
    INVALID_BITBUCKET_FORMAT = 'Please enter a valid bitbucket url. Url should start with https://bitbucket.org'
    BITBUCKET_EXISTS = 'An application with this bitbucket already exists'
    INVALID_BITBUCKET_LENGTH = 'Bitbucket URL cannot exceed 200 characters'
    SERVER_NOT_SELECTED = 'Please select a server'
    NAME_EXISTS = 'An application with this name already exists'
    INVALID_NAME_LENGTH = 'Name cannot exceed 150 characters'
    INVALID_NAME_FORMAT = 'Application name must only contain alphabetic characters and hyphens'
    INVALID_TEAM_NAME_FORMAT = 'Team name must only contain alphabetic characters hyphens'
    INVALID_TEAM_LENGTH = 'Development team name cannot exceed 150 characters'
    INVALID_TEAM_EMAIL_LENGTH = 'Development team email cannot exceed 150 characters'
    INVALID_EXTRA_INFO_LENGTH = 'Extra Information cannot exceed 1000 characters'