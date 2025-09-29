from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Person(BaseModel):
    id: int
    name: str
    allowed: bool
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True  # permite criar a partir de objetos ORM

class PersonCreate(BaseModel):
    name: str
    allowed: bool
    notes: Optional[str] = ""  # se tiver notas
    timestamp: Optional[datetime] = None  # agora opcional

class PersonImageSchema(BaseModel):
    id: int
    person_id: int
    image_base64: str
    embedding: List[float]
    timestamp: datetime

    class Config:
        orm_mode = True
