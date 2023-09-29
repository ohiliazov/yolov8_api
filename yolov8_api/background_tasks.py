import shutil

import httpx
import torch
from loguru import logger
from ultralytics import YOLO

from .constants import ModelStatus
from .exceptions import InvalidModelSource, ModelDownloadError
from .logic import ModelManager
from .models import Model, Project, Sample


def download_model(manager: ModelManager, model: Model):
    manager.update_model_status(model, ModelStatus.DOWNLOADING)
    logger.info(f"Downloading model id={model.id} from {model.url}...")
    client = httpx.Client(follow_redirects=True)
    try:
        with client.stream("GET", url=model.url) as response:
            with open(model.path, mode="wb") as model_file:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    model_file.write(chunk)
    except Exception as err:
        manager.update_model_status(model, ModelStatus.INVALID)
        raise ModelDownloadError() from err

    logger.info(f"Validating model id={model.id} from {model.url}...")
    try:
        YOLO(model.path, task=model.task_type)
    except Exception as err:
        logger.exception(f"Model id={model.id} is invalid!")
        manager.update_model_status(model, ModelStatus.INVALID)
        shutil.rmtree(model.path, ignore_errors=True)
        raise InvalidModelSource(str(err))

    logger.info(f"Model id={model.id} is valid.")
    manager.update_model_status(model, ModelStatus.VALID)


def run_predictions_on_sample(sample: Sample) -> None:
    if not sample.prediction_path.exists():
        model = YOLO(sample.project.model.path, task=sample.project.model.task_type)
        result = model.predict(sample.image_path)
        torch.save(result, sample.prediction_path)


def run_predictions_on_project(project: Project) -> None:
    model = YOLO(project.model.path, task=project.model.task_type)
    for sample in project.samples:
        if not sample.prediction_path.exists():
            result = model.predict(sample.image_path)
            torch.save(result, sample.prediction_path)
