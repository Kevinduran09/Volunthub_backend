from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.models.inscriptionModel import InscriptionModel
from app.repositories.inscription_repository import InscriptionRepository
from datetime import datetime, timezone


class InscriptionAlreadyExistsError(Exception):
    pass


class InscriptionNotFoundError(Exception):
    pass


class InscriptionService:
    def __init__(self, db: AsyncSession):
        self.repo = InscriptionRepository(db=db)

    async def create_inscription(self, user_id: int, event_id: int):
        # Verificar si ya existe la inscripción
        existing = await self.repo.get_by_user_and_event(user_id, event_id)
        if existing:
            raise InscriptionAlreadyExistsError(
                f"User {user_id} is already inscribed in event {event_id}"
            )

        entity = InscriptionModel(id_user=user_id, id_event=event_id)
        return await self.repo.create(entity)

    async def delete_inscription(self, user_id: int, event_id: int) -> bool:
        inscription = await self.repo.get_by_user_and_event(user_id, event_id)
        if not inscription:
            return False

        return await self.repo.delete(inscription.id)

    async def get_inscriptions_by_event(self, event_id: int):
        return await self.repo.get_by_event_id(event_id)

    async def get_inscriptions_by_user(self, user_id: int):
        return await self.repo.get_by_user_id(user_id)

    async def count_inscriptions_by_event(self, event_id: int) -> int:
        return await self.repo.count_by_event_id(event_id)

    async def count_inscriptions_by_event_ids(
        self, event_ids: list[int]
    ) -> dict[int, int]:
        return await self.repo.count_by_event_ids(event_ids)

    async def check_user_inscribed(self, user_id: int, event_id: int) -> bool:
        inscription = await self.repo.get_by_user_and_event(user_id, event_id)
        return inscription is not None
