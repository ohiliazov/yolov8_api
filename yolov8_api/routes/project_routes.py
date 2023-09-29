from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy.exc import NoResultFound

from ..background_tasks import run_predictions_on_project
from ..dependencies import ProjectManagerDep
from ..schemas import ProjectCreate, ProjectRead

router = APIRouter(tags=["Projects"])


@router.post("/projects", response_model=ProjectRead)
def create_project(
    manager: ProjectManagerDep,
    data: ProjectCreate,
):
    try:
        project = manager.create_project(data)
    except Exception as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(err))

    return project


@router.get("/projects", response_model=list[ProjectRead])
def list_user_projects(manager: ProjectManagerDep):
    return manager.list_projects()


@router.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(manager: ProjectManagerDep, project_id: int):
    try:
        return manager.get_project(project_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/projects/{project_id}", response_model=ProjectRead)
def delete_project(manager: ProjectManagerDep, project_id: int):
    try:
        return manager.delete_project(project_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("/projects/{project_id}/predict", status_code=status.HTTP_202_ACCEPTED)
def predict_on_project(
    manager: ProjectManagerDep, project_id: int, background_tasks: BackgroundTasks
):
    try:
        project = manager.get_project(project_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    background_tasks.add_task(run_predictions_on_project, project)

    return {"status": "accepted"}
