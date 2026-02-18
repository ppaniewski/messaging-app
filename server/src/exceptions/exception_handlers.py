from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import BadRequestException, UnauthorizedException, NotFoundException, ServerErrorException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request, exc: BadRequestException):
        return JSONResponse(status_code=exc.code, content={"detail": str(exc)})
    
    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request, exc: UnauthorizedException):
        return JSONResponse(status_code=exc.code, content={"detail": str(exc)})

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request, exc: NotFoundException):
        return JSONResponse(status_code=exc.code, content={"detail": str(exc)})
    
    @app.exception_handler(ServerErrorException)
    async def server_error_exception_handler(request, exc: ServerErrorException):
        return JSONResponse(status_code=exc.code, content={"detail": str(exc)})