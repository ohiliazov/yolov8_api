from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
from sqlalchemy.exc import NoResultFound

from ..background_tasks import run_predictions_on_sample
from ..dependencies import SampleManagerDep
from ..schemas import SampleRead

router = APIRouter(tags=["Samples"])


@router.post("/projects/{project_id}/samples", response_model=SampleRead)
async def upload_sample(project_id: int, file: UploadFile, manager: SampleManagerDep):
    try:
        return await manager.create_sample(project_id, file)
    except NoResultFound:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Project with ID '{project_id}' not found.",
        )


@router.get("/projects/{project_id}/samples", response_model=list[SampleRead])
def list_project_samples(manager: SampleManagerDep, project_id: int):
    return manager.list_project_samples(project_id)


@router.delete("/projects/{project_id}/samples", response_model=list[SampleRead])
def delete_project_samples(manager: SampleManagerDep, project_id: int):
    return manager.delete_project_samples(project_id)


@router.get("/projects/{project_id}/samples/{sample_id}", response_model=SampleRead)
def get_project_sample(manager: SampleManagerDep, sample_id: int):
    try:
        return manager.get_project_sample(sample_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete("/projects/{project_id}/samples/{sample_id}", response_model=SampleRead)
def delete_project_sample(manager: SampleManagerDep, sample_id: int):
    try:
        return manager.delete_project_sample(sample_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post(
    "/projects/{project_id}/samples/{sample_id}/predict",
    status_code=status.HTTP_202_ACCEPTED,
)
def predict_on_sample(
    manager: SampleManagerDep,
    sample_id: int,
    background_tasks: BackgroundTasks,
):
    try:
        sample = manager.get_project_sample(sample_id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    background_tasks.add_task(run_predictions_on_sample, sample)

    return {"status": "accepted"}
