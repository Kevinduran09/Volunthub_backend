from __future__ import annotations

from datetime import date as DateType, datetime, time as TimeType, timezone
from typing import Any, Optional

from pydantic import (
    BaseModel,
    Field,
    AliasChoices,
    ConfigDict,
    field_validator,
    model_validator,
    ValidationInfo,
)


class EventCreateORMArgs(BaseModel):
    """
    Exposes ORM column names (including current typos), while accepting
    Spanish/English payload keys via AliasChoices.
    """
    model_config = ConfigDict(extra="ignore")

    title: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("title", "titulo"))
    description: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("description", "descripcion"))

    date: Optional[DateType] = Field(
        default=None, validation_alias=AliasChoices("date", "fecha"))
    time_begin: Optional[TimeType] = Field(
        default=None,
        validation_alias=AliasChoices(
            "start_time", "hora_inicio", "time_begin"),
    )

    zone: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("timezone", "zone", "zona"))
    address: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("address", "direccion"))

    # Converted to PostGIS Geography(Point, 4326) if parse_location is provided in context.
    location: Any = Field(
        default=None, validation_alias=AliasChoices("location", "ubicacion"))

    require_volunters: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices(
            "requires_volunteers", "requiere_voluntarios", "require_volunters"),
    )
    volunters_required: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices(
            "required_participants_count",
            "cantidad_participantes_requeridos",
            "volunters_required",
        ),
    )

    image_url: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("image_url"))
    materials_required: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "required_materials", "materiales_requeridos", "materials_required"),
    )
    skills_required: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "required_skills", "habilidades_requeridas", "skills_required"),
    )
    extra_data: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "additional_requirements", "requisitos_adicionales", "extra_data"),
    )

    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @field_validator("time_begin", mode="before")
    @classmethod
    def parse_time(cls, v):
        if v is None or isinstance(v, TimeType):
            return v
        if isinstance(v, str):
            for fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    return datetime.strptime(v, fmt).time()
                except ValueError:
                    continue
        return None

    @model_validator(mode="after")
    def convert_location(self, info: ValidationInfo):
        parse_location = info.context.get(
            "parse_location") if info.context else None
        if callable(parse_location) and isinstance(self.location, dict):
            self.location = parse_location(self.location)
        return self
