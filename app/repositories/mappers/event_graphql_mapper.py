from app.graphql.types.event import EventType, LocationType, ParticipantType
from app.infrastructure.models.eventModel import EventModel
from app.infrastructure.models.inscriptionModel import InscriptionModel
from typing import Optional
from datetime import date, time, datetime


def format_date(value) -> str:
    """Formatea una fecha a string ISO"""
    if value is None:
        return ""
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)


def format_time(value) -> str:
    """Formatea una hora a string HH:MM:SS"""
    if value is None:
        return ""
    if isinstance(value, time):
        return value.strftime("%H:%M:%S")
    if isinstance(value, datetime):
        return value.time().strftime("%H:%M:%S")
    return str(value)


def to_graphql_event(
    model: EventModel,
    registered_participants_count: Optional[int] = None,
    distance_meters: Optional[float] = None,
    is_registered: Optional[bool] = None,
    location: Optional[LocationType] = None,
    participants: Optional[list[ParticipantType]] = None,
    tasks: Optional[list] = None,
    category_id: Optional[int] = None,
    created_by_user_id: Optional[int] = None,
) -> EventType:
    """Convert EventModel to GraphQL EventType."""

    event_date = format_date(model.date)
    start_time = format_time(model.time_begin)

    location_value = (
        location if location is not None else getattr(model, "location", None)
    )
    participants_list = participants
    tasks_list = tasks

    return EventType(
        id=str(model.id),
        title=model.title or "",
        description=model.description or "",
        event_date=event_date,
        start_time=start_time,
        timezone=model.zone,
        created_at=model.created_at,
        address=model.address,
        requires_volunteers=model.require_volunters or False,
        required_participants_count=model.volunters_required,
        image_url=model.image_url,
        distance_meters=distance_meters,
        required_materials=model.materials_required,
        required_skills=model.skills_required,
        additional_requirements=model.extra_data,
        _location_value=location_value,
        _registered_participants_count=registered_participants_count,
        _is_registered=is_registered,
        _participants=participants_list,
        _tasks=tasks_list,
        _category_id=category_id
        if category_id is not None
        else getattr(model, "category_id", None) or getattr(model, "categoria", None),
        _created_by_user_id=created_by_user_id
        if created_by_user_id is not None
        else getattr(model, "created_by_user_id", None)
        or getattr(model, "creado_por", None)
        or getattr(model, "created_by", None),
    )


def to_graphql_participante(inscription: InscriptionModel) -> ParticipantType:
    """Convert InscriptionModel to ParticipantType."""
    registered_at = ""
    return ParticipantType(
        user_id=str(inscription.id_user),
        event_id=str(inscription.id_event),
        registered_at=registered_at,
    )
