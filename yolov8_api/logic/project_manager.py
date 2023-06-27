from typing import Sequence

from sqlalchemy.orm import Session

from ..crud import CRUDProjects
from ..models import Project, User
from ..schemas import ProjectCreate


class ProjectManager:
    def __init__(self, db: Session, user: User):
        self.crud = CRUDProjects(db)
        self.user = user

    def create_project(self, data: ProjectCreate) -> Project:
        return self.crud.create_project(self.user, data)

    def list_projects(self) -> Sequence[Project]:
        return self.crud.list_projects(self.user)

    def delete_projects(self):
        return self.crud.delete_projects(self.user)

    def get_project(self, project_id: int) -> Project:
        return self.crud.get_project(self.user, project_id)

    def delete_project(self, project_id: int) -> Project:
        return self.crud.delete_project(self.user, project_id)
