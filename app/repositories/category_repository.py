from .base_repository import BaseRepository
from app.infrastructure.models.categoryModel import CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class CategoryRepository(BaseRepository[CategoryModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = select(CategoryModel)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[CategoryModel]:
        return await self.db.get(CategoryModel, id)

    async def create(self, entity: CategoryModel) -> CategoryModel:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, id: int, update_data: dict) -> CategoryModel:
        existing = await self.db.get(CategoryModel, id)
        if not existing:
            raise ValueError(f"Category with id {id} not found in database")

        for key, value in update_data.items():
            if value is not None:
                setattr(existing, key, value)

        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete(self, id: int) -> bool:
        existing = await self.db.get(CategoryModel, id)
        if not existing:
            return False

        self.db.delete(existing)
        await self.db.commit()
        return True
