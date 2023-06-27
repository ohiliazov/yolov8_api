from enum import StrEnum, auto
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
STATIC_ROOT = PROJECT_ROOT / "static"
MODELS_ROOT = STATIC_ROOT / "models"
IMAGES_ROOT = STATIC_ROOT / "images"
PREDICTIONS_ROOT = STATIC_ROOT / "predictions"


class TaskType(StrEnum):
    DETECT = "detect"
    SEGMENT = "segment"
    CLASSIFY = "classify"


class ModelStatus(StrEnum):
    CREATED = auto()
    DOWNLOADING = auto()
    VALID = auto()
    INVALID = auto()


class ProjectStatus(StrEnum):
    IDLE = auto()
    RUNNING = auto()
