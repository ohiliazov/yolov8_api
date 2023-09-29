import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..constants import ProjectStatus
from .model_schemas import ModelRead


class ProjectCreate(BaseModel):
    name: str = Field(examples=["YOLOv8 Nano Detector Project"])
    model_id: int

    model_config = ConfigDict(protected_namespaces=())


class ProjectRead(BaseModel):
    id: int
    created_at: datetime.datetime
    name: str = Field(examples=["YOLOv8 Nano Detector Project"])
    status: ProjectStatus
    model: ModelRead

    model_config = ConfigDict(from_attributes=True)
