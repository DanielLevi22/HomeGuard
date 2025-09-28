from fastapi import APIRouter, Depends, HTTPException,Form,UploadFile,File
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from schemas.person import Person, PersonCreate
import crud.person as crud

router = APIRouter(prefix="/Persons", tags=["Persons"])

@router.post("/", response_model=Person)
async def create_person_endpoint(
    name: str = Form(...),
    allowed: bool = Form(...),
    notes: str = Form(""),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ler bytes da imagem
    image_bytes = await image.read()

    # Criar objeto para CRUD
    person_create = PersonCreate(
        name=name,
        allowed=allowed,
        notes=notes,
        image_data=image_bytes
    )

    # Criar no banco
    db_person = crud.create_person(db, person_create)
    return db_person

@router.get("/", response_model=List[Person])
def list_Persons(db: Session = Depends(get_db)):
    return crud.get_Persons(db)

@router.get("/{Person_id}", response_model=Person)
def get_Person(Person_id: int, db: Session = Depends(get_db)):
    Person = crud.get_Person(db, Person_id)
    if not Person:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return Person

@router.put("/{Person_id}", response_model=Person)
def update_Person(Person_id: int, Person_data: dict, db: Session = Depends(get_db)):
    Person = crud.update_Person(db, Person_id, Person_data)
    if not Person:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return Person

@router.delete("/{Person_id}")
def delete_Person(Person_id: int, db: Session = Depends(get_db)):
    success = crud.delete_Person(db, Person_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return {"ok": True}
