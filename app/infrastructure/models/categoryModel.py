from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
