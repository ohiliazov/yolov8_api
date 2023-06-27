import datetime
import uuid

from pydantic import BaseModel, HttpUrl

from ..constants import ModelStatus, TaskType


class ModelCreate(BaseModel):
    name: str
    task_type: TaskType
    url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "name": "YOLOv8 Nano Model",
                "url": (
                    "https://github.com/ultralytics/assets/releases/download/v0.0.0"
                    "/yolov8n.pt"
                ),
                "task_type": "detect",
            },
        }


class ModelInsert(BaseModel):
    name: str
    task_type: TaskType
    url: str
    filename: str

    class Config:
        schema_extra = {
            "example": {
                "name": "YOLOv8 Nano Model",
                "task_type": "detect",
                "url": (
                    "https://github.com/ultralytics/assets/releases/download/v0.0.0"
                    "/yolov8n.pt"
                ),
                "filename": f"{uuid.uuid4()}.pt",
            },
        }


class ModelRead(BaseModel):
    id: int
    created_at: datetime.datetime
    name: str
    task_type: TaskType
    url: HttpUrl
    status: ModelStatus

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2023-06-29T18:09:30.734713",
                "name": "YOLOv8 Nano Model",
                "task_type": "detect",
                "url": (
                    "https://github.com/ultralytics/assets/releases/download/v0.0.0"
                    "/yolov8n.pt"
                ),
                "status": ModelStatus.VALID.value,
            },
        }


class ModelClassesRead(BaseModel):
    classes: dict[int, str] | None
