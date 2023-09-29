from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_uri: str = "sqlite:///db.sqlite3"
    debug_mode: bool = True
    secret_key: str = "5111278f4f697d9d0ee0937ad4f920e418df732a74b98e5e4551976e9dee5332"
    jwt_algorithm: str = "HS256"


env = Settings()
