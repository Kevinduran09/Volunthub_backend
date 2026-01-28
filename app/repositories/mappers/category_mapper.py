from app.graphql.types.category import CategoryType
from app.infrastructure.models.categoryModel import CategoryModel


def to_graphql_category(model: CategoryModel) -> CategoryType:
    return CategoryType(
        id=str(model.id),
        name=model.name or "",
        description=model.description,
    )
