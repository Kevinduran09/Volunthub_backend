from app.domain.user import User
from app.infrastructure.models.userModel import UserModel


def to_domain_user(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
        email=model.email,
        avatar_url=model.avatar_url
    )
