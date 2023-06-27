from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..dependencies import CurrentUserDep, UserManagerDep
from ..schemas import Token, UserCreate, UserRead
from ..utils import create_access_token, verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def sign_up(manager: UserManagerDep, data: UserCreate):
    try:
        user = manager.create_user(data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{data.username}' already taken.",
        )

    return user


@router.post("/sign-in", response_model=Token)
def sign_in(
    request: Request,
    manager: UserManagerDep,
    data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = manager.get_user_by_username(data.username)
    except NoResultFound:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(user.username)

    request.session["token"] = token

    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def account_info(user: CurrentUserDep):
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(manager: UserManagerDep, user: CurrentUserDep):
    manager.delete_user(user)
