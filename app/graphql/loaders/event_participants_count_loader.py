from aiodataloader import DataLoader

from app.services.inscription_service import InscriptionService


class EventParticipantsCountLoader(DataLoader):
    def __init__(self, service: InscriptionService):
        super().__init__()
        self.service = service

    async def batch_load_fn(self, event_ids):
        if not event_ids:
            return []
        event_ids_int = [int(event_id) for event_id in event_ids]
        counts_map = await self.service.count_inscriptions_by_event_ids(event_ids_int)
        return [counts_map.get(event_id, 0) for event_id in event_ids_int]
