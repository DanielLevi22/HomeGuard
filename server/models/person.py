from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    allowed = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    # Relacionamento 1:N → uma pessoa pode ter vários embeddings
    images = relationship("PersonImage", back_populates="person", cascade="all, delete-orphan")


class PersonImage(Base):
    __tablename__ = "person_images"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    image_base64 = Column(String, nullable=False)  # imagem salva em base64
    embedding = Column(JSON, nullable=False)       # lista de floats
    timestamp = Column(DateTime, default=datetime.now, nullable=False)

    person = relationship("Person", back_populates="images")