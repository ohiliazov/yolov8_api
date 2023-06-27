from sqlalchemy import select

from ..models import User
from ..schemas import UserInsert
from .crud_base import CRUDBase


class CRUDUsers(CRUDBase[User]):
    model = User

    def create_user(self, data: UserInsert) -> User:
        user = User(**data.dict())
        return self.add(user)

    def get_user_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = self.db.execute(stmt)
        return result.scalar_one()

    def delete_user(self, user: User):
        self.delete(user)
