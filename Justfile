debug := env_var_or_default("DEBUG", "")

# default recipe to display help information
default:
  @just --list

# install poetry dependencies
install:
    poetry install --sync


# upgrade database to the latest revision
upgrade:
    poetry run alembic upgrade head


# downgrade database to the previous revision
downgrade:
    poetry run alembic downgrade -1


# make new database revision
revision message="revision":
    poetry run alembic revision --autogenerate -m {{message}}


# run development server
up host="127.0.0.1" port="8000":
    poetry run uvicorn --factory yolov8_api.main:create_app --host {{host}} --port {{port}} {{ if debug =~ "yes|1|true|on" {"--reload"} else {""} }}
