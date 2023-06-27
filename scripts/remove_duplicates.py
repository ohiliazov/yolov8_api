import filecmp
import os
from collections import defaultdict
from pathlib import Path

from sqlalchemy import select, update

from yolov8_api.constants import IMAGES_ROOT, MODELS_ROOT, PREDICTIONS_ROOT
from yolov8_api.database import get_db
from yolov8_api.models import Model, Sample


def find_duplicates(folder: Path) -> defaultdict[str, list[str]]:
    filenames = os.listdir(folder)
    found = set()
    result = defaultdict(list)

    for idx, file1 in enumerate(filenames, start=1):
        if file1 in found:
            continue

        for file2 in filenames[idx:]:
            if file2 in found:
                continue

            if filecmp.cmp(folder / file1, folder / file2):
                found.add(file2)
                result[file1].append(file1)

    return result


model_duplicates = find_duplicates(MODELS_ROOT)
image_duplicates = find_duplicates(IMAGES_ROOT)
prediction_duplicates = find_duplicates(PREDICTIONS_ROOT)

session = next(get_db())

for original_filename, duplicate_filenames in model_duplicates.items():
    stmt = (
        update(Model)
        .where(Model.filename.in_(duplicate_filenames))
        .values(filename=original_filename)
    )
    session.execute(stmt)

for original_filename, duplicate_filenames in image_duplicates.items():
    stmt = (
        update(Sample)
        .where(Sample.image_filename.in_(duplicate_filenames))
        .values(image_filename=original_filename)
    )
    session.execute(stmt)

for original_filename, duplicate_filenames in image_duplicates.items():
    stmt = (
        update(Sample)
        .where(Sample.prediction_filename.in_(duplicate_filenames))
        .values(prediction_filename=original_filename)
    )
    session.execute(stmt)

session.commit()


models = set(session.execute(select(Model.filename)).scalars().all())
images = set(session.execute(select(Sample.image_filename)).scalars().all())
predictions = set(session.execute(select(Sample.prediction_filename)).scalars().all())

for path in set(os.listdir(MODELS_ROOT)) - models:
    os.remove(MODELS_ROOT / path)

for path in set(os.listdir(IMAGES_ROOT)) - images:
    os.remove(IMAGES_ROOT / path)

for path in set(os.listdir(PREDICTIONS_ROOT)) - predictions:
    os.remove(PREDICTIONS_ROOT / path)
