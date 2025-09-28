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
    embedding = Column(JSON, nullable=True)  # Armazena embedding atual (lista de 512 floats)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)  # Data de cadastro/atualização
    # camera_id = Column(String, nullable=True)  # ID da câmera (ex: "cam1")

    # # Relacionamento com tabela de histórico de embeddings
    # embedding_history = relationship("PersonEmbeddingHistory", back_populates="person")

# class PersonEmbeddingHistory(Base):
#     __tablename__ = "person_embedding_history"

#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
#     embedding = Column(JSON, nullable=False)  # Embedding antigo
#     timestamp = Column(DateTime, default=datetime.now, nullable=False)  # Data do embedding

#     # Relacionamento inverso
#     person = relationship("Person", back_populates="embedding_history")