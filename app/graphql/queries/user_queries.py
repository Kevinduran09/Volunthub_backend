import strawberry
from strawberry.types import Info
from app.services.user_service import UserService
from app.repositories.mappers.user_mapper import to_domain_user
from app.graphql.types.user import UserType
from app.graphql.context import GraphQLContext


@strawberry.type
class UsuarioQueries:
    @strawberry.field
    async def usuario(self, info: Info[GraphQLContext], id: strawberry.ID) -> UserType:

        service = info.context.services.user_service

        entity = await service.get_user(int(str(id)))
        return to_domain_user(entity) if entity else None

    @strawberry.field
    async def usuarios(self, info: Info[GraphQLContext], busqueda: str | None = None) -> list[UserType]:

        service = info.context.services.user_service

        entities = await service.list_users(busqueda)
        return [to_domain_user(u) for u in entities]
