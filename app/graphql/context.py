from typing import AsyncGenerator
from fastapi import Request
from app.graphql.loaders.event_participants_count_loader import (
    EventParticipantsCountLoader,
)
from app.infrastructure.core.database import AsyncSessionLocal
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.depends.container import ServiceContainer
from strawberry.fastapi import BaseContext


@dataclass
class Loaders:
    event_participants_count: EventParticipantsCountLoader


@dataclass
class GraphQLContext(BaseContext):
    request: Request
    db: AsyncSession
    services: "ServiceContainer"
    logger: object
    loaders: Loaders


async def get_context(request: Request) -> AsyncGenerator[GraphQLContext, None]:
    async with AsyncSessionLocal() as db:
        logger = object()
        services = ServiceContainer(db=db, logger=logger)
        loaders = Loaders(
            event_participants_count=EventParticipantsCountLoader(
                services.inscription_service
            )
        )
        yield GraphQLContext(
            request=request,
            db=db,
            services=services,
            logger=logger,
            loaders=loaders,
        )
