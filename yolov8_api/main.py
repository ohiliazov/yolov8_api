from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from .config import env
from .constants import IMAGES_ROOT, MODELS_ROOT, PREDICTIONS_ROOT, STATIC_ROOT
from .routes import auth_routes, model_routes, project_routes, sample_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="YOLOv8 API",
        description="YOLOv8 Object Detection API",
        debug=env.debug_mode,
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=env.secret_key,
        max_age=None,
    )

    app.include_router(auth_routes.router)
    app.include_router(model_routes.router)
    app.include_router(project_routes.router)
    app.include_router(sample_routes.router)

    @app.on_event("startup")
    def create_static_folders():
        STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        MODELS_ROOT.mkdir(exist_ok=True)
        IMAGES_ROOT.mkdir(exist_ok=True)
        PREDICTIONS_ROOT.mkdir(exist_ok=True)

    return app


app = create_app()
