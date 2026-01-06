from .base_repository import BaseRepository
from app.infrastructure.models.userModel import UserModel

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from sqlalchemy import select


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[UserModel]:
        stmt = select(UserModel).order_by(UserModel.id.desc)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id):
        return await self.db.get(UserModel, id)

    async def create(self, entity):
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, id: int, update_data: dict):
        existing = await self.db.get(UserModel, id)

        if not existing:
            raise ValueError(f"User with id {id} not found in database")

        # Actualizar solo los campos presentes en update_data (filtrando None)
        # Esto permite actualizaciones parciales sin if tras if
        for key, value in update_data.items():
            if value is not None:
                setattr(existing, key, value)

        await self.db.commit()
        await self.db.refresh(existing)

        return existing

    async def delete(self, id: int) -> bool:
        existing = await self.db.get(UserModel, id)

        if not existing:
            return False

        await self.db.delete(existing)
        await self.db.commit()

        return True

    async def get_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)

        result = await self.db.execute(stmt)

        print(result)
        return result.scalars().first()

    async def search(self, criterio: str | None, limit: int = 50, offset: int = 0):
        stmt = select(UserModel)

        if criterio:
            like = f"%{criterio.strip()}"
            stmt = stmt.where((UserModel.name.ilike(like)) |
                              (UserModel.email.ilike(like)))
        stmt = stmt.order_by(UserModel.id.desc()).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
