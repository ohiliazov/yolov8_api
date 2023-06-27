from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Base

DBModel = TypeVar("DBModel", bound=Base)


class CRUDBase(Generic[DBModel]):
    model: Type[DBModel]

    def __init__(self, db: Session):
        self.db = db

    def add(self, instance: DBModel) -> DBModel:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, instance_id: int) -> DBModel:
        stmt = select(self.model).where(self.model.id == instance_id)
        result = self.db.execute(stmt)
        return result.scalar_one()

    def delete(self, instances: DBModel | Sequence[DBModel]) -> None:
        if not isinstance(instances, Sequence):
            instances = [instances]

        for instance in instances:
            self.db.delete(instance)
        self.db.commit()
