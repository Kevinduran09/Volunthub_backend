class Ubicacion:
    def __init__(self, latitud: float | None, longitud: float | None):
        self.latitud = latitud
        self.longitud = longitud


class Event:
    def __init__(
        self,
        id: int,
        title: str | None,
        description: str | None,
        date,
        time_begin,
        zone: str | None,
        created_at: str | None,
        address: str | None,
        ubicacion: Ubicacion | None,
        require_volunters: bool | None,
        volunters_required: int | None,
        image_url: str | None,
        materials_required: str | None,
        skills_required: str | None,
        extra_data: str | None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.time_begin = time_begin
        self.zone = zone
        self.created_at = created_at
        self.address = address
        self.ubicacion = ubicacion
        self.require_volunters = require_volunters
        self.volunters_required = volunters_required
        self.image_url = image_url
        self.materials_required = materials_required
        self.skills_required = skills_required
        self.extra_data = extra_data
