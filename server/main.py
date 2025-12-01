from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from src.models.base import init_models
from server.src.routers import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router)