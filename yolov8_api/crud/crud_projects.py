from typing import Sequence

from sqlalchemy import select

from ..models import Project, User
from ..schemas import ProjectCreate
from .crud_base import CRUDBase


class CRUDProjects(CRUDBase[Project]):
    model = Project

    def create_project(self, user: User, data: ProjectCreate) -> Project:
        project = Project(user=user, **data.dict())
        return self.add(project)

    def list_projects(self, user: User) -> Sequence[Project]:
        stmt = select(Project).where(Project.user == user)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def delete_projects(self, user: User) -> Sequence[Project]:
        projects = self.list_projects(user)
        self.delete(projects)
        return projects

    def get_project(self, user: User, project_id: int) -> Project:
        stmt = select(Project).where(Project.id == project_id, Project.user == user)
        result = self.db.execute(stmt)
        return result.scalar_one()

    def delete_project(self, user: User, project_id: int) -> Project:
        project = self.get_project(user, project_id)
        self.delete(project)
        return project
