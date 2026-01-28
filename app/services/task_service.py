from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db=db)

    async def get_tasks_by_event(self, event_id: int):
        return await self.repo.get_by_event_id(event_id)
