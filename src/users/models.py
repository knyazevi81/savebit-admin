from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from src.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    class Config:
        from_attributes = True