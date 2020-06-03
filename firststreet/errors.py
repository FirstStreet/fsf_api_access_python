# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

RATE_LIMIT = 'Request rate limited. Free for non-commercial use for up to 10 requests per minute! To increase ' \
             'your rate limit, please contact api@firststreet.com'
UNAUTHORIZED = 'Unauthorized Access. invalid API key provided.'
UNKNOWN = 'Unknown error, please check your request and try again.'
INTERNAL = 'Internal Server Error.'
NO_BODY = 'No body returned from response.'
NOT_FOUND = 'The specified object could not be found.'
OFFLINE = 'API is currently offline, try again later.'
NOT_ACCEPTABLE = 'You requested a format that is\'t JSON.'
NETWORK_ERROR = 'Network error, check host name.'
DEFAULT_ERROR = 'Unknown Client error.'
ENDPOINT_ERROR = 'HTTP Error: No endpoint provided for request.'
INVALID_ARGUMENT = 'Argument provided was invalid.'


class FirstStreetError(Exception):

    def __init__(self, message=DEFAULT_ERROR, attachments=None):
        super().__init__(message)
        self.message = message
        self.attachments = attachments


class RateLimitError(FirstStreetError):

    def __init__(self, message=RATE_LIMIT, attachments=None):
        super().__init__(message, attachments)


class UnauthorizedError(FirstStreetError):

    def __init__(self, message=UNAUTHORIZED, attachments=None):
        super().__init__(message, attachments)


class UnknownError(FirstStreetError):

    def __init__(self, message=UNKNOWN, attachments=None):
        super().__init__(message, attachments)


class InternalError(FirstStreetError):

    def __init__(self, message=INTERNAL, attachments=None):
        super().__init__(message, attachments)


class NoBodyError(FirstStreetError):

    def __init__(self, message=NO_BODY, attachments=None):
        super().__init__(message, attachments)


class NotFoundError(FirstStreetError):

    def __init__(self, message=NOT_FOUND, attachments=None):
        super().__init__(message, attachments)


class OfflineError(FirstStreetError):

    def __init__(self, message=OFFLINE, attachments=None):
        super().__init__(message, attachments)


class NotAcceptableError(FirstStreetError):

    def __init__(self, message=NOT_ACCEPTABLE, attachments=None):
        super().__init__(message, attachments)


class NetworkError(FirstStreetError):

    def __init__(self, message=NETWORK_ERROR, attachments=None):
        super().__init__(message, attachments)


class EndpointError(FirstStreetError):

    def __init__(self, message=ENDPOINT_ERROR, attachments=None):
        super().__init__(message, attachments)


class InvalidArgument(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = INVALID_ARGUMENT + " Provided Arg: %s" % message


class MissingAPIKeyError(Exception):
    pass
