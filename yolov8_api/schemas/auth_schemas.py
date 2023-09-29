from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str = Field(examples=["johndoe"])
    password: str = Field(examples=["Qwerty!123"])


class UserInsert(BaseModel):
    username: str
    hashed_password: str


class UserRead(BaseModel):
    username: str = Field(examples=["johndoe"])
    disabled: bool

    model_config = ConfigDict(from_attributes=True)
