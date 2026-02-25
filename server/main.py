from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
import socketio

load_dotenv()

from src.models.base import init_models
from src.routers import auth_router, user_router, conversation_router
from src.exceptions.exception_handlers import register_exception_handlers
from src.websocket.events import register_socketio_events

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    yield

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(conversation_router.router)

sio = socketio.AsyncServer(
    async_mode="asgi"
)
register_socketio_events(sio)

app = socketio.ASGIApp(sio, app)