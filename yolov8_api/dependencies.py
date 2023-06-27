from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from .database import get_db
from .logic import ModelManager, ProjectManager, SampleManager, UserManager
from .models import User
from .utils import parse_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign-in", auto_error=False)

DatabaseDep = Annotated[Session, Depends(get_db)]


def extract_token_from_headers_or_cookies(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> str:
    if token:
        request.session["token"] = token

    try:
        return request.session["token"]
    except KeyError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


def get_user_manager(db: DatabaseDep) -> UserManager:
    return UserManager(db)


UserManagerDep = Annotated[UserManager, Depends(get_user_manager)]


def get_current_user(
    manager: UserManagerDep,
    token: str = Depends(extract_token_from_headers_or_cookies),
) -> User:
    try:
        token_data = parse_access_token(token)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    try:
        user = manager.get_user_by_username(token_data.username)
    except NoResultFound:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if user.disabled:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_model_manager(db: DatabaseDep, user: CurrentUserDep) -> ModelManager:
    return ModelManager(db, user)


def get_project_manager(db: DatabaseDep, user: CurrentUserDep) -> ProjectManager:
    return ProjectManager(db, user)


def get_sample_manager(db: DatabaseDep, user: CurrentUserDep) -> SampleManager:
    return SampleManager(db, user)


ModelManagerDep = Annotated[ModelManager, Depends(get_model_manager)]
ProjectManagerDep = Annotated[ProjectManager, Depends(get_project_manager)]
SampleManagerDep = Annotated[SampleManager, Depends(get_sample_manager)]
