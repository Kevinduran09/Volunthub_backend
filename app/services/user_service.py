
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.models.userModel import UserModel

from app.repositories.user_repository import UserRepository


class UserAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, db: AsyncSession, logger):
        self.repo = UserRepository(db=db)
        self.logger = logger

    async def create_user(self, name: str, email: str):
        existing = await self.repo.get_by_email(email=email)

        if existing:
            raise UserAlreadyExistsError("email already exists")

        entity = UserModel(name=name, email=email)
        return await self.repo.create(entity=entity)

    async def list_users(self, criterio: str | None):
        return await self.repo.search(criterio)

    async def get_user(self, user_id: int):
        return await self.repo.get_by_id(user_id)

    async def update_user(self, user_id: int, update_data: dict):
        # Verificar que el usuario existe
        existing_user = await self.repo.get_by_id(user_id)
        if not existing_user:
            raise ValueError(f"User with id {user_id} not found")

        # Si se está actualizando el email, verificar que no exista otro usuario con ese email
        if "email" in update_data:
            user_with_email = await self.repo.get_by_email(update_data["email"])
            if user_with_email and user_with_email.id != user_id:
                raise UserAlreadyExistsError("Email already exists")

        # Los campos ya vienen en el formato correcto (name, email, avatar_url)
        # El repositorio maneja las actualizaciones parciales automáticamente
        return await self.repo.update(user_id, update_data)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)
