from sqlalchemy.orm import Session
from models.person import Person as PersonModel
from schemas.person import PersonCreate

def create_Person(db: Session, Person: PersonCreate):
    db_Person = PersonModel(**Person.dict())
    db.add(db_Person)
    db.commit()
    db.refresh(db_Person)
    return db_Person

def get_Persons(db: Session):
    return db.query(PersonModel).all()

def get_Person(db: Session, Person_id: int):
    return db.query(PersonModel).filter(PersonModel.id == Person_id).first()

def delete_Person(db: Session, Person_id: int):
    Person = get_Person(db, Person_id)
    if Person:
        db.delete(Person)
        db.commit()
        return True
    return False

def update_Person(db: Session, Person_id: int, updates: dict):
    Person = get_Person(db, Person_id)
    if not Person:
        return None
    for key, value in updates.items():
        setattr(Person, key, value)
    db.commit()
    db.refresh(Person)
    return Person
