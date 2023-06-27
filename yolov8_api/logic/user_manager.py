from sqlalchemy.orm import Session

from ..crud import CRUDUsers
from ..models import User
from ..schemas import UserCreate, UserInsert
from ..utils import get_password_hash


class UserManager:
    def __init__(self, db: Session):
        self.crud = CRUDUsers(db)

    def create_user(self, user_create: UserCreate) -> User:
        user_insert = UserInsert(
            username=user_create.username,
            hashed_password=get_password_hash(user_create.password),
        )
        return self.crud.create_user(user_insert)

    def get_user_by_username(self, username: str) -> User:
        return self.crud.get_user_by_username(username)

    def delete_user(self, user: User):
        self.crud.delete(user)
