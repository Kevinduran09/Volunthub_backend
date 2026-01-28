import strawberry
from strawberry.types import Info

from app.graphql.context import GraphQLContext
from app.graphql.types.category import CategoryType
from app.repositories.mappers.category_mapper import to_graphql_category


@strawberry.type
class CategoriaQueries:
    @strawberry.field
    async def categorias(self, info: Info[GraphQLContext]) -> list[CategoryType]:
        service = info.context.services.category_service
        categories = await service.get_all_categories()
        return [to_graphql_category(category) for category in categories]

    @strawberry.field
    async def categoria(
        self, info: Info[GraphQLContext], id: strawberry.ID
    ) -> CategoryType | None:
        service = info.context.services.category_service
        category = await service.get_category_by_id(int(str(id)))
        return to_graphql_category(category) if category else None
