from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from src.database import Base


class Servers(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(unique=True, nullable=False)
    server_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    port: Mapped[str] = mapped_column(nullable=False) # if host have tls use 443
    basepath: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    class Config:
        from_attributes = True