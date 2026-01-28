from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.eventDto import EventCreateORMArgs
from app.infrastructure.models.eventModel import EventModel
from app.infrastructure.models.taskModel import TaskModel
from app.repositories.event_repository import EventRepository
from app.repositories.inscription_repository import InscriptionRepository
from app.repositories.category_repository import CategoryRepository
from app.services.inscription_service import InscriptionService
from datetime import datetime, date, time
from typing import Optional
from app.infrastructure.helpers.geo_adapter import parse_location


class EventService:
    def __init__(self, db: AsyncSession):
        self.repo = EventRepository(db=db)
        self.inscription_repo = InscriptionRepository(db=db)
        self.category_repo = CategoryRepository(db=db)
        self.inscription_service = InscriptionService(db=db)

    async def get_events(self, busqueda: str | None = None):
        return await self.repo.search(busqueda)

    async def get_events_paginated(
        self, busqueda: str | None = None, page: int = 1, per_page: int = 6
    ):
        events, total = await self.repo.search_paginated(busqueda, page, per_page)
        return {"eventos": events, "total": total}

    async def get_event_by_id(self, event_id: int):
        return await self.repo.get_by_id(event_id)

    async def get_events_by_category(self, category_id: int):
        return await self.repo.get_by_category(category_id)

    async def get_nearby_events(self, lat: float, lon: float, radius: int = 10000):
        return await self.repo.get_nearby_events(lat, lon, radius)

    async def get_users_inscribed_in_event(self, event_id: int):
        inscriptions = await self.inscription_repo.get_by_event_id(event_id)
        from app.infrastructure.models.userModel import UserModel

        user_ids = [ins.id_user for ins in inscriptions]
        if not user_ids:
            return []

        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession

        # Necesitamos acceso a db, lo obtenemos del repositorio
        db: AsyncSession = self.repo.db
        stmt = select(UserModel).where(UserModel.id.in_(user_ids))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_next_events_by_user(self, user_id: int):
        return await self.repo.get_upcoming_user_events(user_id)

    async def create_event(self, event_data: dict, user_id: int):
        dto = EventCreateORMArgs.model_validate(
            event_data, context={"parse_location": parse_location}
        )
        entity = EventModel(**dto.model_dump())

        tasks_payload = event_data.get("tasks") or []

        for task in tasks_payload:
            entity.tasks.append(
                TaskModel(
                    title=task["name"],
                    description=task.get("description"),
                    priority=task.get("priority"),
                    status="pendint",
                )
            )

        return await self.repo.create(entity)

    async def subscribe_to_event(self, event_id: int, user_id: int):
        return await self.inscription_service.create_inscription(user_id, event_id)

    async def unsubscribe_from_event(self, event_id: int, user_id: int) -> bool:
        return await self.inscription_service.delete_inscription(user_id, event_id)

    async def check_user_subscribed(self, event_id: int, user_id: int) -> bool:
        return await self.inscription_service.check_user_inscribed(user_id, event_id)

    async def get_event_participants_count(self, event_id: int) -> int:
        return await self.inscription_service.count_inscriptions_by_event(event_id)
