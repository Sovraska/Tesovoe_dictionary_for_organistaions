from typing import Iterator

from sqlalchemy import func

from core.db.models import Organisation, Building
from core.db.repository.organisation import OrganisationRepository


class OrganisationService:
    def __init__(self, organisation_repository: OrganisationRepository) -> None:
        self._repository: OrganisationRepository = organisation_repository

    async def get_organisations(self) -> Iterator[Organisation]:
        return await self._repository.get_all()

    async def get_organisation_by_id(self, organisation_id: int) -> Organisation:
        return await self._repository.get_by_id(organisation_id)

    # async def delete_organisation_by_id(self, organisation_id: int) -> None:
    #     return await self._repository.delete_by_id(organisation_id)

    async def get_by_activity_organisations(self, activity_name):
        return await self._repository.get_by_activity(activity_name)

    async def get_by_name_organisations(self, organisation_name):
        return await self._repository.get_by_name(organisation_name)

    async def get_by_location_organisation(self, latitude, longitude, radius):
        # Earth diameter KM
        R = 12_742 / 2

        target_lat_rad = func.radians(latitude)
        target_lon_rad = func.radians(longitude)

        # Haversine formula (SQL)
        distance = (
                R * func.acos(
            func.least(1.0,
                       func.cos(target_lat_rad) * func.cos(func.radians(Building.latitude))
                       * func.cos(func.radians(Building.longitude) - target_lon_rad) +
                       func.sin(target_lat_rad) * func.sin(func.radians(Building.latitude))
                       )
        )
        )
        return await self._repository.get_by_location(distance, radius)

    async def get_by_building_name_organisations(self, building_address):
        return await self._repository.get_by_building_name(building_address)

    async def get_by_activity_tree_organisation(self, activity_name):
        return await self._repository.get_by_activity_tree(activity_name)
