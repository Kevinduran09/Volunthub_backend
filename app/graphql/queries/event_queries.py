import strawberry
from strawberry.types import Info
from app.graphql.context import GraphQLContext
from app.graphql.types.event import EventType, PaginatedEventsType, LocationType
from app.repositories.mappers.event_graphql_mapper import to_graphql_event
from app.repositories.mappers.user_mapper import to_domain_user
from app.graphql.types.user import UserType
from typing import Optional
# Intentar importar geoalchemy2 para extraer ubicación de PostGIS
try:
    from geoalchemy2.shape import to_shape
    HAS_GEO_SHAPE = True
except ImportError:
    HAS_GEO_SHAPE = False


@strawberry.type
class EventoQueries:
    @strawberry.field
    async def eventos(
        self, info: Info[GraphQLContext], busqueda: Optional[str] = None
    ) -> list[EventType]:
        service = info.context.services.event_service
        events = await service.get_events(busqueda)

        result = []
        for event in events:
            # Contar participantes inscritos
            count = await service.get_event_participants_count(event.id)

            # Convertir evento a GraphQL
            event_gql = to_graphql_event(
                event,
                participantes_inscritos=count,
            )
            result.append(event_gql)

        return result

    @strawberry.field
    async def eventosPaginados(
        self,
        info: Info[GraphQLContext],
        busqueda: Optional[str] = None,
        page: int = 1,
        perPage: int = 6,
    ) -> PaginatedEventsType:
        service = info.context.services.event_service
        result = await service.get_events_paginated(busqueda, page, perPage)

        eventos_gql = []
        for event in result["eventos"]:
            count = await service.get_event_participants_count(event.id)
            event_gql = to_graphql_event(event, participantes_inscritos=count)
            eventos_gql.append(event_gql)

        return PaginatedEventsType(
            eventos=eventos_gql,
            total=result["total"]
        )

    @strawberry.field
    async def evento(
        self, info: Info[GraphQLContext], id: strawberry.ID
    ) -> Optional[EventType]:
        service = info.context.services.event_service
        event = await service.get_event_by_id(int(str(id)))

        if not event:
            return None

        count = await service.get_event_participants_count(event.id)

        # Extraer ubicación de PostGIS si está disponible
        ubicacion = None
        if HAS_GEO_SHAPE:
            try:
                if event.location is not None:
                    point = to_shape(event.location)
                    if hasattr(point, 'x') and hasattr(point, 'y'):
                        ubicacion = LocationType(
                            latitud=str(point.y),
                            longitud=str(point.x)
                        )
            except Exception:
                ubicacion = None

        return to_graphql_event(event, participantes_inscritos=count, ubicacion=ubicacion)

    @strawberry.field
    async def eventosPorCategoria(
        self, info: Info[GraphQLContext], categoria: strawberry.ID
    ) -> list[EventType]:
        service = info.context.services.event_service
        events = await service.get_events_by_category(int(str(categoria)))

        result = []
        for event in events:
            count = await service.get_event_participants_count(event.id)
            event_gql = to_graphql_event(event, participantes_inscritos=count)
            result.append(event_gql)

        return result

    @strawberry.field
    async def eventosCercanos(
        self,
        info: Info[GraphQLContext],
        lat: float,
        lon: float,
        radio: Optional[int] = None,
    ) -> list[EventType]:
        service = info.context.services.event_service
        radius = radio if radio is not None else 10000  # Default 10km
        events = await service.get_nearby_events(lat, lon, radius)

        result = []
        for event in events:
            count = await service.get_event_participants_count(event.id)
            # Obtener distancia del atributo agregado por el repositorio
            distancia_m = getattr(event, 'distance_m', None)

            event_gql = to_graphql_event(
                event,
                participantes_inscritos=count,
                distancia_m=distancia_m,
            )
            result.append(event_gql)

        return result

    @strawberry.field
    async def UsuariosInscritosAUnEvento(
        self, info: Info[GraphQLContext], idEvento: strawberry.ID
    ) -> list[UserType]:
        service = info.context.services.event_service
        users = await service.get_users_inscribed_in_event(int(str(idEvento)))

        from app.repositories.mappers.user_mapper import to_domain_user
        return [to_domain_user(user) for user in users]

    @strawberry.field
    async def nextsEventByUser(
        self,
        info: Info[GraphQLContext],
        usuarioId: Optional[strawberry.ID] = None,
    ) -> list[EventType]:
        service = info.context.services.event_service

        # TODO: Obtener userId del contexto cuando se implemente autenticación
        # user_id = info.context.get("userId") or int(str(usuarioId))
        user_id = int(str(usuarioId)) if usuarioId else None

        if not user_id:
            return []

        events = await service.get_next_events_by_user(user_id)

        result = []
        for event in events:
            count = await service.get_event_participants_count(event.id)
            event_gql = to_graphql_event(event, participantes_inscritos=count)
            result.append(event_gql)

        return result
