from app.domain.task import Task
from app.infrastructure.models.taskModel import TaskModel


def to_domain_task(model: TaskModel) -> Task:
    return Task(
        id=model.id,
        title=model.title,
        status=model.status,
        description=model.description,
        priority=model.priority,
        event_id=model.event_id,
        completed_by=model.completed_by,
    )
