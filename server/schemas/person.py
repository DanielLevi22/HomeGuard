from pydantic import BaseModel

class Person(BaseModel):
    id: int
    name: str
    allowed: bool
    notes: str
    class Config:
        from_attributes = True  

class PersonCreate(BaseModel):
    name: str
    allowed: bool
    notes: str
