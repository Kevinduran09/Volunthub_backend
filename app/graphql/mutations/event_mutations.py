import strawberry
from strawberry.types import Info
from strawberry.exceptions import GraphQLError
from app.graphql.context import GraphQLContext
from app.graphql.types.event import CreateEventInput, EventType
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
            event_data = asdict(input) if is_dataclass(input) else dict(input)
            request = info.context.request
            user_id = getattr(request, "user_id", None)
            if user_id is None and hasattr(request, "state"):
                user_id = getattr(request.state, "user_id", None)
            if not user_id:
                user_id = int(str(input.organizer_id)) if input.organizer_id else None
            if not user_id:
                raise GraphQLError("Authentication required")

            event = await service.create_event(event_data, int(user_id))

            return to_graphql_event(event)

        except ValueError as e:
            raise GraphQLError(str(e))
        except GraphQLError:
            raise
        except Exception as e:
            raise GraphQLError(f"Error interno creando evento: {str(e)}")

    @strawberry.mutation
    async def inscribirse(
        self,
        info: Info[GraphQLContext],
        eventoId: strawberry.ID,
    ) -> bool:
        service = info.context.services.event_service

        try:
            # request = info.context.request
            # user_id = getattr(request, "user_id", None)
            # if user_id is None and hasattr(request, "state"):
            #     user_id = getattr(request.state, "user_id", None)
            # if not user_id:
            #     return False
            user_id = 1
            event_id = int(str(eventoId))
            await service.subscribe_to_event(event_id, int(user_id))
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
            event_id = int(str(eventoId))
            if usuarioId:
                user_id = int(str(usuarioId))
            else:
                request = info.context.request
                user_id = getattr(request, "user_id", None)
                if user_id is None and hasattr(request, "state"):
                    user_id = getattr(request.state, "user_id", None)
            if not user_id:
                return False

            return await service.unsubscribe_from_event(event_id, int(user_id))

        except Exception as e:
            if isinstance(e, GraphQLError):
                raise
            raise GraphQLError(f"Error al anular inscripción: {str(e)}")
