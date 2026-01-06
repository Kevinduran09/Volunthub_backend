from app.domain.event import Event, Ubicacion
from app.infrastructure.models.eventModel import EventModel


def to_domain_event(model: EventModel) -> Event:
    ubicacion = None
    # Extraer lat/lon del Geography de PostGIS
    # Nota: Por ahora dejamos ubicacion como None
    # Se implementará la extracción de PostGIS Geography cuando se necesite
    # Para extraer: usar geoalchemy2.shape.to_shape(model.location)
    # si model.location is not None:

    return Event(
        id=model.id,
        title=model.title,
        description=model.description,
        date=model.date,
        time_begin=model.time_begin,
        zone=model.zone,
        created_at=model.created_at,
        address=model.address,
        ubicacion=ubicacion,
        require_volunters=model.require_volunters,
        volunters_required=model.volunters_required,
        image_url=model.image_url,
        materials_required=model.materials_required,
        skills_required=model.skills_required,
        extra_data=model.extra_data,
    )
