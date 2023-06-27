import datetime

from pydantic import BaseModel

from ..constants import ProjectStatus
from .model_schemas import ModelRead


class ProjectCreate(BaseModel):
    name: str
    model_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": "YOLOv8 Nano Detector Project",
                "model_id": 1,
            },
        }


class ProjectRead(BaseModel):
    id: int
    created_at: datetime.datetime
    name: str
    status: ProjectStatus
    model: ModelRead

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2023-07-10T17:16:35.523642",
                "name": "YOLOv8 Nano Detector Project",
                "status": ProjectStatus.IDLE,
                "model": ModelRead.Config.schema_extra["example"],
            },
        }
