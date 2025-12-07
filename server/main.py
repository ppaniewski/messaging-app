from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from src.models.base import init_models
from src.routers import auth_router, user_router, conversation_router
from src.exceptions.exception_handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    register_exception_handlers(app)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(conversation_router.router)