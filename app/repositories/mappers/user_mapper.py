from app.graphql.types.user import UserType
from app.infrastructure.models.userModel import UserModel


def to_domain_user(model: UserModel) -> UserType:
    return UserType(
        id=str(model.id),
        name=model.name,
        email=model.email,
        avatar_url=model.avatar_url
    )
