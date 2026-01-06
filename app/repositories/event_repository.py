from .base_repository import BaseRepository
from app.infrastructure.models.eventModel import EventModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date


class EventRepository(BaseRepository[EventModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[EventModel]:
        stmt = select(EventModel).order_by(EventModel.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[EventModel]:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.inscriptions))
            .where(EventModel.id == id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, entity: EventModel) -> EventModel:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, id: int, update_data: dict) -> EventModel:
        existing = await self.db.get(EventModel, id)
        if not existing:
            raise ValueError(f"Event with id {id} not found in database")

        for key, value in update_data.items():
            if value is not None:
                setattr(existing, key, value)

        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete(self, id: int) -> bool:
        existing = await self.db.get(EventModel, id)
        if not existing:
            return False

        self.db.delete(existing)
        await self.db.commit()
        return True

    async def search(self, busqueda: str | None = None) -> List[EventModel]:
        stmt = select(EventModel)
        if busqueda:
            like = f"%{busqueda.strip()}%"
            stmt = stmt.where(
                (EventModel.title.ilike(like)) | (
                    EventModel.description.ilike(like))
            )
        stmt = stmt.order_by(EventModel.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search_paginated(
        self, busqueda: str | None = None, page: int = 1, per_page: int = 6
    ) -> tuple[List[EventModel], int]:
        # Query base
        base_stmt = select(EventModel)
        if busqueda:
            like = f"%{busqueda.strip()}%"
            base_stmt = base_stmt.where(
                (EventModel.title.ilike(like)) | (
                    EventModel.description.ilike(like))
            )

        # Contar total
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        # Obtener resultados paginados
        offset = (page - 1) * per_page
        stmt = base_stmt.order_by(EventModel.id.desc()).offset(
            offset).limit(per_page)
        result = await self.db.execute(stmt)
        events = list(result.scalars().all())

        return events, total

    async def get_by_category(self, category_id: int) -> List[EventModel]:
        # Nota: Si EventModel tiene campo category_id, usarlo. Por ahora asumimos que no existe
        # TODO: Agregar category_id al modelo si es necesario
        stmt = select(EventModel).order_by(EventModel.id.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_nearby_events(
        self, lat: float, lon: float, radius_meters: int = 10000
    ) -> List[EventModel]:
        """
        Obtiene eventos cercanos usando PostGIS geography.
        radius_meters: radio en metros (por defecto 10km)
        """
        # Crear punto de referencia usando WKT
        point_wkt = f"POINT({lon} {lat})"

        # Usar ST_Distance con geography (devuelve metros)
        stmt = (
            select(
                EventModel,
                func.ST_Distance(
                    EventModel.location,
                    func.ST_GeogFromText(text(f"'SRID=4326;{point_wkt}'"))
                ).label("distance_m")
            )
            .where(
                func.ST_DWithin(
                    EventModel.location,
                    func.ST_GeogFromText(text(f"'SRID=4326;{point_wkt}'")),
                    radius_meters
                )
            )
            .order_by("distance_m")
        )

        result = await self.db.execute(stmt)
        rows = result.all()
        # Extraer eventos y agregar distancia como atributo
        events = []
        for row in rows:
            event = row[0]
            event.distance_m = float(row[1]) if row[1] else None
            events.append(event)

        return events

    async def get_user_events(self, user_id: int) -> List[EventModel]:
        """Obtiene eventos en los que el usuario está inscrito"""
        from app.infrastructure.models.inscriptionModel import InscriptionModel

        stmt = (
            select(EventModel)
            .join(InscriptionModel, EventModel.id == InscriptionModel.id_event)
            .where(InscriptionModel.id_user == user_id)
            .order_by(EventModel.date.desc(), EventModel.time_begin.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_upcoming_user_events(self, user_id: int) -> List[EventModel]:
        """Obtiene próximos eventos del usuario (fecha >= hoy)"""
        from app.infrastructure.models.inscriptionModel import InscriptionModel

        today = date.today()
        stmt = (
            select(EventModel)
            .join(InscriptionModel, EventModel.id == InscriptionModel.id_event)
            .where(InscriptionModel.id_user == user_id)
            .where(EventModel.date >= today)
            .order_by(EventModel.date.asc(), EventModel.time_begin.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
