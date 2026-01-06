from typing import TYPE_CHECKING, List
from geoalchemy2 import Geography
from sqlalchemy import Boolean, Date, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.core.database import Base

if TYPE_CHECKING:
    # solo para typing, no en runtime
    from app.infrastructure.models.taskModel import TaskModel


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)

    date: Mapped[str | None] = mapped_column(Date)
    time_begin: Mapped[str | None] = mapped_column(Time)

    zone: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str | None] = mapped_column(String)
    address: Mapped[str | None] = mapped_column(Text)

    location = mapped_column(Geography(geometry_type="POINT", srid=4326))

    require_volunters: Mapped[bool | None] = mapped_column(Boolean)
    volunters_required: Mapped[int | None] = mapped_column(Integer)

    image_url: Mapped[str | None] = mapped_column(String)
    materials_required: Mapped[str | None] = mapped_column(String)
    skills_required: Mapped[str | None] = mapped_column(String)
    extra_data: Mapped[str | None] = mapped_column(String)

    # Relaciones
    inscriptions = relationship("InscriptionModel", back_populates="event")
    tasks: Mapped[List["TaskModel"]] = relationship(
        "TaskModel",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
