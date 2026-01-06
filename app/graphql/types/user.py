import strawberry
from strawberry import UNSET


@strawberry.type
class UserType:
    id: strawberry.ID
    name: str
    email: str
    avatar_url: str | None


@strawberry.type
class UserStats:
    totalEventos: int
    totalTareasCompletadas: int
    totalEventosCreados: int


@strawberry.input
class CreateUserInput:
    name: str
    email: str


@strawberry.input
class UpdateUserInput:
    name: str | None = UNSET
    email: str | None = UNSET
    avatar_url: str | None = UNSET
