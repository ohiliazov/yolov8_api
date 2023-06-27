from datetime import datetime
from pathlib import Path

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from .constants import (
    IMAGES_ROOT,
    MODELS_ROOT,
    PREDICTIONS_ROOT,
    ModelStatus,
    ProjectStatus,
    TaskType,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    models: Mapped[list["Model"]] = relationship(viewonly=True)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"

    @property
    def model_count(self) -> int:
        return len(self.models)


class HasUser:
    """
    Mark classes that have many-to-one relationship to the "User" class.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    @declared_attr
    def user(self) -> Mapped["User"]:
        return relationship("User")


class Model(Base, HasUser):
    __tablename__ = "model"

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[ModelStatus] = mapped_column(default=ModelStatus.CREATED)
    name: Mapped[str]
    task_type: Mapped[TaskType]
    url: Mapped[str]
    filename: Mapped[str]

    projects: Mapped[list["Project"]] = relationship(back_populates="model")

    def __repr__(self):
        return f"Model(id={self.id!r}, name={self.name!r}, status={self.status!r})"

    @property
    def path(self):
        return MODELS_ROOT / self.filename


class Project(Base, HasUser):
    __tablename__ = "project"

    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))

    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.IDLE)

    model: Mapped[Model] = relationship(back_populates="projects")
    samples: Mapped[list["Sample"]] = relationship(back_populates="project")

    def __repr__(self):
        return f"Project(id={self.id!r}, name={self.name!r}, status={self.status!r})"


class Sample(Base):
    __tablename__ = "sample"

    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    image_filename: Mapped[str]
    prediction_filename: Mapped[str]

    project: Mapped[Project] = relationship(back_populates="samples")

    def __repr__(self):
        return (
            f"Sample(id={self.id!r}, image_filename={self.image_filename!r}, "
            f"prediction_filename={self.prediction_filename!r})"
        )

    @property
    def image_path(self) -> Path:
        return IMAGES_ROOT / self.image_filename

    @property
    def prediction_path(self) -> Path:
        return PREDICTIONS_ROOT / self.prediction_filename
