from pydantic import BaseModel, Field
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserCreate(BaseModel):
    username: str
    password: str


@router.post("register", status_code=201)
async def register_user(user: UserCreate): 
    return ""
