from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy.exc import NoResultFound

from ..background_tasks import download_model
from ..dependencies import ModelManagerDep
from ..schemas import ModelCreate, ModelRead
from ..schemas.model_schemas import ModelClassesRead

router = APIRouter(tags=["Models"])


@router.post("/models", response_model=ModelRead)
def create_model(
    manager: ModelManagerDep,
    data: ModelCreate,
    background_tasks: BackgroundTasks,
):
    try:
        model = manager.create_model(data)
    except Exception as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(err))

    background_tasks.add_task(download_model, manager, model)

    return model


@router.get("/models", response_model=list[ModelRead])
def list_user_models(manager: ModelManagerDep):
    return manager.list_models()


@router.delete("/models", response_model=list[ModelRead])
def delete_user_models(manager: ModelManagerDep):
    return manager.delete_models()


@router.get("/models/{model_id}", response_model=ModelRead)
def get_model(manager: ModelManagerDep, model_id: int):
    try:
        return manager.get_model(model_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/models/{model_id}", response_model=ModelRead)
def delete_model(manager: ModelManagerDep, model_id: int):
    try:
        return manager.delete_model(model_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get("/models/{model_id}/classes", response_model=ModelClassesRead)
def get_model_classes(manager: ModelManagerDep, model_id: int):
    try:
        return manager.get_model_classes(model_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
