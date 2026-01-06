from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService


class ServiceContainer:
    def __init__(self, db: AsyncSession, logger):
        self._db = db
        self._logger = logger
        self._cache: dict[str, object] = {}

    def _get(self, key: str, factory):
        if key not in self._cache:
            self._cache[key] = factory()
        return self._cache[key]

    @property
    def user_service(self) -> UserService:
        from app.services.user_service import UserService
        return self._get("usuario_service", lambda: UserService(self._db, self._logger))

    @property
    def event_service(self):
        from app.services.event_service import EventService
        return self._get("event_service", lambda: EventService(self._db))

    @property
    def category_service(self):
        from app.services.category_service import CategoryService
        return self._get("category_service", lambda: CategoryService(self._db))

    @property
    def inscription_service(self):
        from app.services.inscription_service import InscriptionService
        return self._get("inscription_service", lambda: InscriptionService(self._db))
