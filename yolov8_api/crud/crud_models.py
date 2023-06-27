from typing import Sequence

from sqlalchemy import select

from ..constants import ModelStatus
from ..models import Model, User
from ..schemas import ModelInsert
from .crud_base import CRUDBase


class CRUDModels(CRUDBase[Model]):
    model = Model

    def create_model(self, user: User, data: ModelInsert) -> Model:
        model = Model(user=user, **data.dict())
        return self.add(model)

    def list_models(self, user: User) -> Sequence[Model]:
        stmt = select(Model).where(Model.user == user)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def delete_models(self, user: User) -> Sequence[Model]:
        models = self.list_models(user)
        self.delete(models)
        return models

    def get_model(self, user: User, model_id: int) -> Model:
        stmt = select(Model).where(
            Model.id == model_id,
            Model.user == user,
        )
        result = self.db.execute(stmt)
        return result.scalar_one()

    def delete_model(self, user: User, model_id: int) -> Model:
        model = self.get_model(user, model_id)
        self.delete(model)
        return model

    def update_model_status(self, model: Model, status: ModelStatus) -> Model:
        model.status = status
        return self.add(model)
