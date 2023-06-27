from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        schema_extra = {"example": {"username": "johndoe", "token_type": "bearer"}}


class TokenData(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "johndoe", "password": "Qwerty!123"}}


class UserInsert(BaseModel):
    username: str
    hashed_password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "hashed_password": (
                    "$2b$12$BQ9FHx5xCt42qpOpqcLfVu8tCPiVfDg0PhElYnrezt4PxaSrvWOJO"
                ),
            }
        }


class UserRead(BaseModel):
    username: str
    disabled: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "disabled": False,
            }
        }
