import uuid

from pydantic import BaseModel


class SampleInsert(BaseModel):
    project_id: int
    image_filename: str
    prediction_filename: str

    class Config:
        schema_extra = {
            "example": {
                "project_id": 1,
                "image_filename": f"{uuid.uuid4()}.jpg",
                "prediction_filename": f"{uuid.uuid4()}.pt",
            }
        }


class SampleRead(BaseModel):
    id: int
    project_id: int

    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "project_id": 1}}
