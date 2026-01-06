import strawberry
from strawberry.types import Info
from strawberry.exceptions import GraphQLError

from app.graphql.types.user import UserType as UsuarioType, CreateUserInput, UpdateUserInput
from app.repositories.mappers.user_mapper import to_domain_user
from app.services.user_service import UserService, UserAlreadyExistsError
from app.graphql.context import GraphQLContext


@strawberry.type
class UsuarioMutations:
    @strawberry.mutation
    async def createUser(self, info: Info[GraphQLContext], input: CreateUserInput) -> UsuarioType:

        service = info.context.services.user_service

        try:
            entity = await service.create_user(name=input.name, email=input.email)
            return to_domain_user(entity)
        except UserAlreadyExistsError as e:
            raise GraphQLError(str(e))
        except Exception:
            # Mensaje controlado para no filtrar detalles internos
            raise GraphQLError("Error interno creando usuario")

    @strawberry.mutation
    async def updateUser(
        self,
        info: Info[GraphQLContext],
        id: strawberry.ID,
        input: UpdateUserInput
    ) -> UsuarioType:

        service = info.context.services.user_service

        try:
            # Convertir el input a diccionario (filtrando None para actualizaciones parciales)
            update_data = {
                k: v for k, v in vars(input).items()
                if v is not None and v is not strawberry.UNSET
            }

            entity = await service.update_user(user_id=int(str(id)), update_data=update_data)
            return to_domain_user(entity)
        except UserAlreadyExistsError as e:
            raise GraphQLError(str(e))
        except ValueError as e:
            raise GraphQLError(str(e))
        except Exception as e:
            # Mensaje controlado para no filtrar detalles internos
            raise GraphQLError("Error interno actualizando usuario")

    @strawberry.mutation
    async def deleteUser(self, info: Info[GraphQLContext], id: strawberry.ID) -> bool:

        service = info.context.services.user_service

        try:
            deleted = await service.delete_user(user_id=int(str(id)))
            return deleted
        except Exception:
            # Mensaje controlado para no filtrar detalles internos
            raise GraphQLError("Error interno eliminando usuario")
