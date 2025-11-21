from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.params import Security
from fastapi.security import APIKeyHeader

from app.container import Container
from core.services.organisation import OrganisationService
from core.utils.headers import ApiKeyDep

org_router = APIRouter(prefix='/org')
api_key_header = APIKeyHeader(name="X-API-Key")


@org_router.get('/')
@inject
async def list_org(
        organisation_service: Annotated[
            OrganisationService, Depends(Provide[Container.organisation_service])
        ],
        api_key: ApiKeyDep,
        activity_name: Optional[str] = None,
        organisation_name: Optional[str] = None,
        building_address: Optional[str] = None,

):
    if building_address:
        res = await organisation_service.get_by_building_name_organisations(building_address)
        return jsonable_encoder(res)
    if activity_name:
        res = await organisation_service.get_by_activity_organisations(activity_name)
        return jsonable_encoder(res)
    if organisation_name:
        res = await organisation_service.get_by_name_organisations(organisation_name)
        return jsonable_encoder(res)
    res = await organisation_service.get_organisations()
    return jsonable_encoder(res)


@org_router.get('/{organisation_id}', responses={200: {"model": None}})
@inject
async def get_by_id_org(
        organisation_id: int,
        organisation_service: Annotated[
            OrganisationService, Depends(Provide[Container.organisation_service])
        ],
        api_key: ApiKeyDep,
):
    res = await organisation_service.get_organisation_by_id(organisation_id)
    return jsonable_encoder(res)


@org_router.get('/location/')
@inject
async def list_all_org_location(
        organisation_service: Annotated[
            OrganisationService, Depends(Provide[Container.organisation_service])
        ],
        api_key: ApiKeyDep,
        latitude: float,
        longitude: float,
        radius: int,
):
    res = await organisation_service.get_by_location_organisation(latitude, longitude, radius)
    return jsonable_encoder(res)


@org_router.get('/activity/')
@inject
async def list_all_tree_activity_org(
        organisation_service: Annotated[
            OrganisationService, Depends(Provide[Container.organisation_service])
        ],
        api_key: ApiKeyDep,
        activity_name: str,
):
    res = res = await organisation_service.get_by_activity_tree_organisation(activity_name)
    return jsonable_encoder(res)
