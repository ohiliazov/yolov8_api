import os
import uuid
from typing import Sequence

from fastapi import UploadFile
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..constants import IMAGES_ROOT
from ..crud import CRUDProjects, CRUDSamples
from ..models import Project, Sample, User
from ..schemas import SampleInsert
from ..utils import download_image


class SampleManager:
    def __init__(self, db: Session, user: User):
        self.crud_projects = CRUDProjects(db)
        self.crud_samples = CRUDSamples(db)
        self.user = user

    def _get_user_project(self, project_id: int) -> Project:
        return self.crud_projects.get_project(self.user, project_id)

    async def create_sample(self, project_id: int, file: UploadFile) -> Sample:
        self._get_user_project(project_id)

        _, ext = os.path.splitext(file.filename)

        sample_uuid = uuid.uuid4()
        image_filename = f"{sample_uuid}{ext}"
        prediction_filename = f"{sample_uuid}.pt"

        await download_image(file, IMAGES_ROOT / image_filename)

        data = SampleInsert(
            project_id=project_id,
            image_filename=image_filename,
            prediction_filename=prediction_filename,
        )
        return self.crud_samples.create_sample(data)

    def list_project_samples(self, project_id: int) -> Sequence[Sample]:
        self._get_user_project(project_id)
        return self.crud_samples.list_project_samples(project_id)

    def delete_project_samples(self, project_id: int) -> Sequence[Sample]:
        self._get_user_project(project_id)
        return self.crud_samples.delete_project_samples(project_id)

    def get_project_sample(self, sample_id: int) -> Sample:
        sample = self.crud_samples.get(sample_id)

        if sample.project.user != self.user:
            raise NoResultFound(sample_id)

        return sample

    def delete_project_sample(self, sample_id: int) -> Sample:
        sample = self.get_project_sample(sample_id)
        if sample:
            self.crud_samples.delete(sample)
        return sample
