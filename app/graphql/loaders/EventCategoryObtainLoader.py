from aiodataloader import DataLoader

from app.services.category_service import CategoryService


class EventCategoryObtainLoader(DataLoader):
    def __ini__(self, service: CategoryService):
        super().__init__()
        self.service = service

    async def batch_load_fn(self, event_ids):
        if not event_ids:
            return []
        event_ids_int = [int(id) for id in event_ids]
        counts_result = self.service.get_category_by_ids(event_ids_int)
