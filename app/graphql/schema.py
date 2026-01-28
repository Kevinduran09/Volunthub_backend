import strawberry
from strawberry.schema.config import StrawberryConfig
from app.graphql.mutations.user_mutatios import UsuarioMutations
from app.graphql.queries.user_queries import UsuarioQueries
from app.graphql.mutations.event_mutations import EventoMutations
from app.graphql.queries.event_queries import EventoQueries
from app.graphql.queries.category_queries import CategoriaQueries


@strawberry.type
class Query(UsuarioQueries, EventoQueries, CategoriaQueries):
    @strawberry.field
    def ping(self) -> str:
        return "pong"


@strawberry.type
class Mutation(UsuarioMutations, EventoMutations):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False)
)
