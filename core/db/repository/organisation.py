from contextlib import AbstractAsyncContextManager

from typing import Callable, Iterator
from sqlalchemy import func, select, and_, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from core.db.models import Organisation, Activity, Building


class OrganisationRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> Iterator[Organisation]:
        async with self.session_factory() as async_session:
            stmt = select(Organisation)
            result = await async_session.execute(stmt)
            return result.scalars().all()

    async def get_by_id(self, organisation_id: int) -> Organisation:
        async with self.session_factory() as async_session:
            stmt = select(Organisation).where(Organisation.id == organisation_id)
            result = await async_session.execute(stmt)
            return result.scalars().first()

    # async def add(self, test: str) -> Organisation:
    #     async with self.session_factory() as async_session:
    #         organisation = Organisation(test=test)
    #         async_session.add(organisation)
    #         await async_session.commit()
    #         await async_session.refresh(organisation)
    #         return organisation
    #
    # async def delete_by_id(self, organisation_id: int) -> None:
    #     async with self.session_factory() as async_session:
    #         stmt = select(Organisation).where(Organisation.id == organisation_id)
    #         result = await async_session.execute(stmt)
    #         await async_session.delete(result)
    #         await async_session.commit()

    async def get_by_activity(self, activity_name):
        async with self.session_factory() as async_session:
            stmt = select(Organisation).join(Organisation.activity).where(Activity.title == activity_name)
            result = await async_session.execute(stmt)
            return result.scalars().first()

    async def get_by_name(self, organisation_name):
        async with self.session_factory() as async_session:
            stmt = select(Organisation).where(Organisation.title == organisation_name)
            result = await async_session.execute(stmt)
            return result.scalars().first()

    async def get_by_location(self, distance, radius):
        async with self.session_factory() as async_session:
            stmt = select(Organisation, distance.label("distance_km")).join(Organisation.building).filter(
                distance <= radius
            ).order_by(distance)

            result = await async_session.execute(stmt)
            return result.scalars().first()

    async def get_by_building_name(self, building_address):
        async with self.session_factory() as async_session:
            stmt = select(Organisation).select_from(Building) \
                .join(Organisation.building) \
                .where(Building.address == building_address)
            result = await async_session.execute(stmt)
            return result.scalars().all()

    async def get_by_activity_tree(self, activity_name):
        async with self.session_factory() as async_session:
            parent_activity = aliased(Activity)
            child_activity = aliased(Activity)

            # CTE иерархия
            activity_hierarchy = (
                select(
                    parent_activity.id,
                    parent_activity.title,
                    literal(1).label("level")  # устанавливаем 1 уровень (ибо 0 уже взяли)
                )
                .where(parent_activity.title == activity_name)
                .cte(name="activity_hierarchy", recursive=True)
            )

            # ограниучение рекурсии до 3х
            child_query = (
                select(
                    child_activity.id,
                    child_activity.title,
                    (activity_hierarchy.c.level + 1).label("level")  # правило инкремента уровня
                )
                .where(
                    and_(
                        child_activity.parent_id == activity_hierarchy.c.id,
                        activity_hierarchy.c.level < 3
                    )
                )
            )
            activity_hierarchy = activity_hierarchy.union_all(child_query)

            # Запрос организаций с найденым деревом активностей
            query = (
                select(Organisation)
                .join(Organisation.activity)
                .where(Activity.id.in_(select(activity_hierarchy.c.id)))
            )

            result = await async_session.execute(query)
            return result.scalars().all()
