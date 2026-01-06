from typing import AsyncGenerator
from fastapi import Request
from app.infrastructure.core.database import AsyncSessionLocal
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.depends.container import ServiceContainer
from strawberry.fastapi import BaseContext


@dataclass
class GraphQLContext(BaseContext):
    request: Request
    db: AsyncSession
    services: "ServiceContainer"
    logger: object  # o el tipo de structlog logger cuando lo montes


async def get_context(request: Request) -> AsyncGenerator[GraphQLContext, None]:
    async with AsyncSessionLocal() as db:
        logger = object()
        services = ServiceContainer(db=db, logger=logger)
        yield GraphQLContext(request=request, db=db, services=services, logger=logger)
