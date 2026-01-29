import strawberry
from typing import Optional
from strawberry.types import Info

from app.graphql.context import GraphQLContext
from app.graphql.types.task import TaskType, TaskInput
from app.graphql.types.user import UserType
from app.graphql.types.category import CategoryType

try:
    from geoalchemy2.shape import to_shape

    HAS_GEO_SHAPE = True
except ImportError:
    to_shape = None
    HAS_GEO_SHAPE = False


@strawberry.type
class LocationType:
    latitude: str
    longitude: str


@strawberry.type
class ParticipantType:
    user_id: strawberry.ID
    event_id: strawberry.ID
    registered_at: str


@strawberry.type
class EventType:
    id: strawberry.ID
    title: str
    description: str
    event_date: str
    start_time: str
    timezone: Optional[str]
    created_at: Optional[str]
    address: Optional[str]
    requires_volunteers: bool
    required_participants_count: Optional[int]
    image_url: Optional[str]
    distance_meters: Optional[float]
    required_materials: Optional[str]
    required_skills: Optional[str]
    additional_requirements: Optional[str]
    _location_value: strawberry.Private[object | None] = None
    _participants: strawberry.Private[Optional[list[ParticipantType]]] = None
    _registered_participants_count: strawberry.Private[Optional[int]] = None
    _tasks: strawberry.Private[Optional[list[TaskType]]] = None
    _is_registered: strawberry.Private[Optional[bool]] = None
    _category_id: strawberry.Private[Optional[int]] = None
    _created_by_user_id: strawberry.Private[Optional[int]] = None

    @strawberry.field
    async def location(self) -> Optional[LocationType]:
        if isinstance(self._location_value, LocationType):
            return self._location_value
        if not HAS_GEO_SHAPE or self._location_value is None or to_shape is None:
            return None
        try:
            point = to_shape(self._location_value)
            if hasattr(point, "x") and hasattr(point, "y"):
                return LocationType(
                    latitude=str(point.y),
                    longitude=str(point.x),
                )
        except Exception:
            return None
        return None

    @strawberry.field
    async def participants(self, info: Info[GraphQLContext]) -> list[ParticipantType]:
        if self._participants is not None:
            return self._participants
        service = info.context.services.inscription_service
        event_id = int(str(self.id))
        inscriptions = await service.get_inscriptions_by_event(event_id)
        return [
            ParticipantType(
                user_id=str(inscription.id_user),
                event_id=str(inscription.id_event),
                registered_at="",
            )
            for inscription in inscriptions
        ]

    @strawberry.field
    async def registered_participants_count(
        self, info: Info[GraphQLContext]
    ) -> Optional[int]:
        if self._registered_participants_count is not None:
            return self._registered_participants_count
        loaders = getattr(info.context, "loaders", None)
        if loaders and hasattr(loaders, "event_participants_count"):
            return await loaders.event_participants_count.load(int(self.id))
        service = info.context.services.event_service
        return await service.get_event_participants_count(int(str(self.id)))

    @strawberry.field
    async def tasks(self, info: Info[GraphQLContext]) -> list[TaskType]:
        if self._tasks is not None:
            return self._tasks
        service = info.context.services.task_service
        event_id = int(str(self.id))
        tasks = await service.get_tasks_by_event(event_id)
        return [
            TaskType(
                id=str(task.id),
                title=task.title or "",
                description=task.description or "",
                status=task.status or "",
                priority=task.priority or "",
                completed_by=str(task.completed_by)
                if task.completed_by is not None
                else "",
                create_at=str(getattr(task, "created_at", ""))
                if getattr(task, "created_at", None) is not None
                else "",
            )
            for task in tasks
        ]

    @strawberry.field
    async def is_registered(self, info: Info[GraphQLContext]) -> Optional[bool]:
        if self._is_registered is not None:
            return self._is_registered
        request = info.context.request
        user_id = getattr(request, "user_id", None)
        if user_id is None and hasattr(request, "state"):
            user_id = getattr(request.state, "user_id", None)
        if not user_id:
            return False
        service = info.context.services.event_service
        return await service.check_user_subscribed(int(str(self.id)), int(user_id))

    @strawberry.field
    async def category(self, info: Info[GraphQLContext]) -> Optional[CategoryType]:
        loaders = getattr(info.context, "loaders", None)
        if loaders and hasattr(loaders, "event_category"):
            return await loaders.event_participants_count.load(int(self.id))
        service = info.context.services.event_service
        return await service.get_event_participants_count(int(str(self.id)))

        return to_graphql_category(category)

    @strawberry.field
    async def created_by(self, info: Info[GraphQLContext]) -> Optional[UserType]:
        if not self._created_by_user_id:
            return None
        service = info.context.services.user_service
        user = await service.get_user(self._created_by_user_id)
        if not user:
            return None
        from app.repositories.mappers.user_mapper import to_domain_user

        return to_domain_user(user)


@strawberry.type
class PaginatedEventsType:
    events: list[EventType]
    total: int


@strawberry.type
class RegistrationType:
    event_id: strawberry.ID
    user_id: strawberry.ID
    registered_at: str


@strawberry.input
class LocationInput:
    latitude: float
    longitude: float


@strawberry.input
class CreateEventInput:
    title: str
    description: str
    date: str
    start_time: str
    timezone: Optional[str] = None
    address: str
    location: LocationInput
    requires_volunteers: bool
    required_participants_count: Optional[int] = None
    image_url: Optional[str] = None
    category_id: int
    required_materials: Optional[str] = None
    required_skills: Optional[str] = None
    additional_requirements: Optional[str] = None
    organizer_id: strawberry.ID
    tasks: Optional[list[TaskInput]] = None
