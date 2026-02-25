from typing import List

from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base_schemas import CamelModel

class UserIn(CamelModel):
    username: str = Field(
        description="Username between 3 and 50 characters long",
        min_length=3, 
        max_length=50
    )
    password: str = Field(
        description="Password between 6 and 64 characters long, must contain at least one character, one digit, and one special symbol", 
        min_length=6, 
        max_length=64
    )

    @field_validator("password")
    def validate_password(cls, v: str):
        if not any([c.isalpha() for c in v]):
            raise ValueError("Must contain a letter")
        if not any([c.isdecimal() for c in v]):
            raise ValueError("Must contain a digit")
        if not any([not c.isalnum() for c in v]):
            raise ValueError("Must contain a symbol")
        
        return v

class UserOut(CamelModel):
    id: int
    username: str

class UserOutConversation(UserOut):
    is_unread: bool

class UserOutLogin(UserOut):
    access_token: str