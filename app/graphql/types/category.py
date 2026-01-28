import strawberry


@strawberry.type
class CategoryType:
    id: strawberry.ID
    name: str
    description: str | None
