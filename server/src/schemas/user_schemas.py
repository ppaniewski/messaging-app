from pydantic import BaseModel, Field, field_validator

class UserIn(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(
        description="Password between 6 and 64 characters, must contain at least one character, one digit, and one special symbol", 
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

class UserOut(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }

class UserOutLogin(UserOut):
    access_token: str