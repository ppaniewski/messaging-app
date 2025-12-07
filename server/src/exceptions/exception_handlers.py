from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .exceptions import BadRequestException, NotFoundException, ServerErrorException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BadRequestException)
    def bad_request_exception_handler(request, exc):
        return JSONResponse(status_code=400, content=exc)

    @app.exception_handler(NotFoundException)
    def not_found_exception_handler(request, exc):
        return JSONResponse(status_code=404, content={"error": exc})
    
    @app.exception_handler(ServerErrorException)
    def server_error_exception_handler(request, exc):
        return JSONResponse(status_code=500, content=exc)