from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base


class InscriptionModel(Base):
    __tablename__ = "inscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_event: Mapped[int] = mapped_column(ForeignKey("events.id"))

    user = relationship("UserModel", back_populates="inscriptions")
    event = relationship("EventModel", back_populates="inscriptions")
