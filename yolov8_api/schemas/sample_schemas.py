import uuid

from pydantic import BaseModel, ConfigDict, Field


class SampleInsert(BaseModel):
    project_id: int
    image_filename: str = Field(examples=[f"{uuid.uuid4()}.jpg"])
    prediction_filename: str = Field(examples=[f"{uuid.uuid4()}.pt"])


class SampleRead(BaseModel):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)
