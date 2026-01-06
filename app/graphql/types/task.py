import strawberry


@strawberry.type
class TaskType:
    id: strawberry.ID
    title: str
    description: str
    status: str
    priority: str
    completed_by: strawberry.ID
    create_at: str


@strawberry.input
class TaskInput:
    name: str
    priority: str
    description: str
