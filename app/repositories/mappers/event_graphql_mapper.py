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
    participantes_inscritos: Optional[int] = None,
    distancia_m: Optional[float] = None,
    esta_inscrito: Optional[bool] = None,
    ubicacion: Optional[LocationType] = None,
    participantes: Optional[list] = None,
    tareas: Optional[list] = None,
    categoria: Optional = None,
    creado_por: Optional = None,
) -> EventType:
    """Convierte EventModel a EventType de GraphQL"""

    # Convertir fecha y hora a strings
    fecha_str = format_date(model.date)
    hora_str = format_time(model.time_begin)

    # Usar ubicacion proporcionada o crear None
    ubicacion_type = ubicacion

    # Usar participantes proporcionados o lista vacía
    participantes_list = participantes if participantes is not None else []

    # Usar tareas proporcionadas o lista vacía
    tareas_list = tareas if tareas is not None else []

    return EventType(
        id=str(model.id),
        titulo=model.title or "",
        descripcion=model.description or "",
        fecha=fecha_str,
        hora_inicio=hora_str,
        zona=model.zone,
        created_at=model.created_at,
        direccion=model.address,
        ubicacion=ubicacion_type,
        requiere_voluntarios=model.require_volunters or False,
        cantidad_participantes_requeridos=model.volunters_required,
        image_url=model.image_url,
        participantes=participantes_list,
        participantes_inscritos=participantes_inscritos,
        distancia_m=distancia_m,
        tareas=tareas_list,
        materiales_requeridos=model.materials_required,
        habilidades_requeridas=model.skills_required,
        requisitos_adicionales=model.extra_data,
        estaInscrito=esta_inscrito,
        categoria=categoria,
        creado_por=creado_por,
    )


def to_graphql_participante(inscription: InscriptionModel) -> ParticipantType:
    """Convierte InscriptionModel a ParticipantesType"""
    from datetime import datetime

    fecha_inscripcion = ""
    # Si hay relación con el evento o se puede obtener de otra forma
    # Por ahora usamos una fecha por defecto o vacía

    return ParticipantType(
        id_usuario=str(inscription.id_user),
        id_evento=str(inscription.id_event),
        fecha_inscripcion=fecha_inscripcion,
    )
