install:
    poetry install --sync


upgrade:
    poetry run alembic upgrade head


downgrade:
    poetry run alembic downgrade -1


revision message="revision":
    poetry run alembic revision --autogenerate -m {{message}}


up host="127.0.0.1" port="8000":
    poetry run uvicorn --factory yolov8_api.main:create_app
