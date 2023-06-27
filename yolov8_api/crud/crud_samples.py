from typing import Sequence

from sqlalchemy import select

from ..models import Sample
from ..schemas.sample_schemas import SampleInsert
from .crud_base import CRUDBase


class CRUDSamples(CRUDBase[Sample]):
    model = Sample

    def create_sample(self, data: SampleInsert) -> Sample:
        sample = Sample(**data.dict())
        return self.add(sample)

    def list_project_samples(self, project_id: int) -> Sequence[Sample]:
        stmt = select(Sample).where(Sample.project_id == project_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def delete_project_samples(self, project_id: int) -> Sequence[Sample]:
        samples = self.list_project_samples(project_id)
        self.delete(samples)
        return samples
