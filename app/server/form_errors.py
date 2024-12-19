from enum import Enum

class ServerFormError(Enum):
    NAME_EXISTS = 'An server with this name already exists'
    INVALID_NAME_FORMAT = 'Server name can only contain letters, numbers and hyphens with no spaces i.e: ab-1234'
    INVALID_NAME_LENGTH = "Server name cannot exceed 50 characters"
    INVALID_LOCATION_LENGTH = 'Location cannot exceed 50 characters'
    INVALID_LOCATION_FORMAT = 'Location can only contain alphabetic characters'