from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.router import main_router


def init_app(fastpi_app: FastAPI) -> FastAPI:
    """Инициализация приложения FastAPI."""
    origins = ["*"]
    fastpi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastpi_app.include_router(main_router)

    return fastpi_app
