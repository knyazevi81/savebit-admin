from src.database import Base
from sqlalchemy import Column, Integer, String, BigInteger


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    class Config:
        orm_mode=True