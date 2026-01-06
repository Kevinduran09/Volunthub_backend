import strawberry
from strawberry.types import Info
from strawberry.exceptions import GraphQLError
from app.graphql.context import GraphQLContext
from app.graphql.types.event import CreateEventInput, LocationInput, TaskInput, EventType
from app.repositories.mappers.event_graphql_mapper import to_graphql_event
from app.repositories.mappers.inscription_mapper import to_domain_inscription
from typing import Optional
from app.services.event_service import EventService
from dataclasses import asdict, is_dataclass


@strawberry.type
class EventoMutations:
    @strawberry.mutation
    async def createEvent(
        self,
        info: Info[GraphQLContext],
        input: CreateEventInput,
    ) -> EventType:
        service: EventService = info.context.services.event_service

        try:
            # TODO: Obtener userId del contexto cuando se implemente autenticación
            # user_id = info.context.get("userId")
            # user_id = int(str(input.organizador_id))
            event_data = asdict(input) if is_dataclass(input) else dict(input)

            event = await service.create_event(event_data, 1)

            # Convertir a GraphQL
            count = await service.get_event_participants_count(event.id)
            return to_graphql_event(event, participantes_inscritos=count)

        except ValueError as e:
            raise GraphQLError(str(e))
        except Exception as e:
            raise GraphQLError(f"Error interno creando evento: {str(e)}")

    @strawberry.mutation
    async def inscribirse(
        self,
        info: Info[GraphQLContext],
        eventoId: strawberry.ID,
    ) -> bool:
        service = info.context.services.event_service
        inscription_service = info.context.services.inscription_service

        try:
            # TODO: Obtener userId del contexto cuando se implemente autenticación
            # user_id = info.context.get("userId")
            # if not user_id:
            #     raise GraphQLError("Usuario no autenticado")
            # Por ahora asumimos que userId está en el contexto o se pasa
            # Necesitaremos ajustar esto cuando tengamos autenticación
            raise GraphQLError(
                "Autenticación requerida - pendiente de implementar")

            event_id = int(str(eventoId))
            inscription = await service.subscribe_to_event(event_id, user_id)

            from datetime import datetime
            fecha_inscripcion = datetime.now().isoformat()

            return True

        except Exception as e:
            if isinstance(e, GraphQLError):
                raise
            raise GraphQLError(f"Error al inscribirse en el evento: {str(e)}")

    @strawberry.mutation
    async def anularInscripcion(
        self,
        info: Info[GraphQLContext],
        eventoId: strawberry.ID,
        usuarioId: Optional[strawberry.ID] = None,
    ) -> bool:
        service = info.context.services.event_service

        try:
            # TODO: Obtener userId del contexto cuando se implemente autenticación
            # user_id = usuarioId or info.context.get("userId")
            # Por ahora requerimos usuarioId
            if not usuarioId:
                raise GraphQLError(
                    "usuarioId es requerido - pendiente autenticación")

            event_id = int(str(eventoId))
            user_id = int(str(usuarioId))

            result = await service.unsubscribe_from_event(event_id, user_id)
            return result

        except Exception as e:
            if isinstance(e, GraphQLError):
                raise
            raise GraphQLError(f"Error al anular inscripción: {str(e)}")
