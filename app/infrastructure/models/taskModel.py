from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str | None] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    priority: Mapped[str | None] = mapped_column(String)

    completed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"))

    event = relationship("EventModel", back_populates="tasks")
    completed_by_user = relationship(
        "UserModel", back_populates="tasks_completed")
