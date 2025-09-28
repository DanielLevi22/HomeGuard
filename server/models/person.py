# models/person.py
from sqlalchemy import Boolean, Column, Integer, String
from core.database import Base  # <- precisa importar o Base daqui

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    allowed = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
