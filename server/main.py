from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.models.base import init_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    yield

app = FastAPI(lifespan=lifespan)