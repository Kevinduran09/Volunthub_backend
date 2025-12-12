from app.domain.inscription import Inscription
from app.infrastructure.models.inscriptionModel import InscriptionModel


def to_domain_inscription(model: InscriptionModel) -> Inscription:
    return Inscription(
        id=model.id,
        id_user=model.id_user,
        id_event=model.id_event,
    )
