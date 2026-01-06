from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.models.categoryModel import CategoryModel
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.repo = CategoryRepository(db=db)

    async def get_category_by_id(self, category_id: int):
        return await self.repo.get_by_id(category_id)

    async def get_all_categories(self):
        return await self.repo.get_all()

    async def create_category(self, name: str, description: str | None = None):
        entity = CategoryModel(name=name, description=description)
        return await self.repo.create(entity)

    async def update_category(self, category_id: int, update_data: dict):
        existing = await self.repo.get_by_id(category_id)
        if not existing:
            raise ValueError(f"Category with id {category_id} not found")
        return await self.repo.update(category_id, update_data)

    async def delete_category(self, category_id: int) -> bool:
        return await self.repo.delete(category_id)
