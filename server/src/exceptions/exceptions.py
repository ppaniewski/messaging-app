class HTTPError(Exception):
    code = 500

class BadRequestException(HTTPError):
    code = 400

class UnauthorizedException(HTTPError):
    code = 401

class NotFoundException(HTTPError):
    code = 404

class ServerErrorException(HTTPError):
    code = 500