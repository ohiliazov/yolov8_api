import os
import uuid
from typing import Sequence

from sqlalchemy.orm import Session
from ultralytics import YOLO

from ..constants import ModelStatus
from ..crud import CRUDModels
from ..models import Model, User
from ..schemas import ModelCreate, ModelInsert
from ..schemas.model_schemas import ModelClassesRead
from ..utils import get_filename_from_url


class ModelManager:
    def __init__(self, db: Session, user: User):
        self.crud = CRUDModels(db)
        self.user = user

    def create_model(self, data: ModelCreate) -> Model:
        _, ext = os.path.splitext(get_filename_from_url(data.url))
        model_path = f"{uuid.uuid4()}{ext}"

        insert_data = ModelInsert(
            **data.dict(),
            filename=str(model_path),
        )

        return self.crud.create_model(self.user, insert_data)

    def list_models(self) -> Sequence[Model]:
        return self.crud.list_models(self.user)

    def delete_models(self):
        return self.crud.delete_models(self.user)

    def get_model(self, model_id: int) -> Model:
        return self.crud.get_model(self.user, model_id)

    def delete_model(self, model_id: int) -> Model:
        return self.crud.delete_model(self.user, model_id)

    def update_model_status(
        self,
        model: Model,
        status: ModelStatus,
    ) -> Model:
        return self.crud.update_model_status(model, status)

    def get_model_classes(self, model_id: int) -> ModelClassesRead:
        model = self.get_model(model_id)
        yolo = YOLO(model.path, task=model.task_type)
        return ModelClassesRead(classes=yolo.names)
