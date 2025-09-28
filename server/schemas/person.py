from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Person(BaseModel):
    id: int
    name: str
    allowed: bool
    notes: Optional[str] = None
    embedding: Optional[list[float]] = None  # Embedding de 512D
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite criar a partir de objetos ORM

class PersonCreate(BaseModel):
    name: str
    allowed: bool
    notes: Optional[str] = None
    image_data: bytes  # Necessário para enviar a imagem na criação
