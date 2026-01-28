from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models.taskModel import TaskModel


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_event_id(self, event_id: int) -> list[TaskModel]:
        stmt = select(TaskModel).where(TaskModel.event_id == event_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
