from .base_repository import BaseRepository
from app.infrastructure.models.inscriptionModel import InscriptionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional


class InscriptionRepository(BaseRepository[InscriptionModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[InscriptionModel]:
        stmt = select(InscriptionModel)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[InscriptionModel]:
        return await self.db.get(InscriptionModel, id)

    async def create(self, entity: InscriptionModel) -> InscriptionModel:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, id: int, update_data: dict) -> InscriptionModel:
        existing = await self.db.get(InscriptionModel, id)
        if not existing:
            raise ValueError(f"Inscription with id {id} not found in database")

        for key, value in update_data.items():
            if value is not None:
                setattr(existing, key, value)

        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete(self, id: int) -> bool:
        existing = await self.db.get(InscriptionModel, id)
        if not existing:
            return False

        self.db.delete(existing)
        await self.db.commit()
        return True

    async def get_by_user_and_event(
        self, user_id: int, event_id: int
    ) -> Optional[InscriptionModel]:
        stmt = select(InscriptionModel).where(
            and_(
                InscriptionModel.id_user == user_id,
                InscriptionModel.id_event == event_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def count_by_event_ids(self, event_ids: list[int]) -> dict[int, int]:
        if not event_ids:
            return {}
        stmt = (
            select(InscriptionModel.id_event, func.count(InscriptionModel.id))
            .where(InscriptionModel.id_event.in_(event_ids))
            .group_by(InscriptionModel.id_event)
        )

        result = await self.db.execute(stmt)
        return {row[0]: row[1] for row in result.all()}

    async def get_by_event_id(self, event_id: int) -> List[InscriptionModel]:
        stmt = select(InscriptionModel).where(
            InscriptionModel.id_event == event_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: int) -> List[InscriptionModel]:
        stmt = select(InscriptionModel).where(
            InscriptionModel.id_user == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_by_event_id(self, event_id: int) -> int:
        stmt = select(func.count(InscriptionModel.id)).where(
            InscriptionModel.id_event == event_id
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0
