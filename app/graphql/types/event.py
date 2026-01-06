import strawberry
from typing import Optional
from app.graphql.types.task import TaskType, TaskInput


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
    location: Optional[LocationType]
    requires_volunteers: bool
    required_participants_count: Optional[int]
    image_url: Optional[str]
    participants: list[ParticipantType]
    registered_participants_count: Optional[int]
    distance_meters: Optional[float]
    tasks: list[TaskType]
    required_materials: Optional[str]
    required_skills: Optional[str]
    additional_requirements: Optional[str]
    is_registered: Optional[bool]
    category_id: Optional[strawberry.ID]
    created_by_user_id: Optional[strawberry.ID]


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
