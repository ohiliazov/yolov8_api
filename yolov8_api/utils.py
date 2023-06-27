from datetime import datetime, timedelta
from pathlib import Path

from fastapi import UploadFile
from jose import jwt
from passlib.context import CryptContext
from pydantic import HttpUrl
from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from .config import env
from .exceptions import InvalidVideoSource
from .schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(username: str) -> str:
    claims = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(weeks=1),
    }

    return jwt.encode(claims, env.secret_key, env.jwt_algorithm)


def parse_access_token(token: str) -> TokenData:
    payload = jwt.decode(token, env.secret_key, env.jwt_algorithm)
    username = payload["sub"]
    return TokenData(username=username)


def get_filename_from_url(url: HttpUrl) -> str:
    return Path(url.path or "").name


def validate_youtube_video_source(url: str):
    try:
        with YoutubeDL({"format": "bestvideo/best"}) as dl:
            dl.extract_info(url, download=False)
    except YoutubeDLError as err:
        raise InvalidVideoSource(str(err))


async def download_image(file: UploadFile, path: Path):
    with open(path, mode="wb") as target_file:
        while chunk := await file.read(1024):
            target_file.write(chunk)


def get_image_with_masks_and_boxes(pred_path: Path):
    pass
