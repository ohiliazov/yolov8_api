import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from ..constants import ModelStatus, TaskType


class ModelCreate(BaseModel):
    name: str = Field(examples=["YOLOv8 Nano Model"])
    task_type: TaskType
    url: HttpUrl = Field(
        examples=[
            "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        ]
    )


class ModelInsert(BaseModel):
    name: str
    task_type: TaskType
    url: str
    filename: str


class ModelRead(BaseModel):
    id: int
    created_at: datetime.datetime
    name: str = Field(examples=["YOLOv8 Nano Model"])
    task_type: TaskType
    url: HttpUrl = Field(
        examples=[
            "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        ]
    )
    status: ModelStatus

    model_config = ConfigDict(from_attributes=True)


class ModelClassesRead(BaseModel):
    classes: dict[int, str] | None
