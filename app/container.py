import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import URL
from dependency_injector import containers, providers

from core.db.repository.organisation import OrganisationRepository
from core.services.organisation import OrganisationService
from core.session import Database

config = load_dotenv()
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = int(os.environ.get('DB_PORT'))

DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
    port=DB_PORT
)


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".api.organisation"])

    #application
    fastapi_app = providers.Singleton(FastAPI)

    # DATABASE
    db = providers.Singleton(Database, db_url=DATABASE_URL)

    # Repositories:
    organisation_repository = providers.Factory(
        OrganisationRepository,
        session_factory=db.provided.session,
    )

    # Services:
    organisation_service = providers.Factory(
        OrganisationService,
        organisation_repository=organisation_repository,
    )
