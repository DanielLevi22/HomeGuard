import cv2
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
from ultralytics import YOLO
from sqlalchemy.orm import Session
from models.person import Person as PersonModel
from schemas.person import PersonCreate
from huggingface_hub import hf_hub_download

# Carregar modelo YOLOv8 localmente
model_path = hf_hub_download(
    repo_id="arnabdhar/YOLOv8-Face-Detection",
    filename="model.pt"
)
yolo_model = YOLO(model_path)

# Inicialize InsightFace fora da função para performance
face_app = FaceAnalysis(providers=['CPUExecutionProvider'])  # Use 'CUDAExecutionProvider' para GPU
face_app.prepare(ctx_id=0, det_size=(640, 640))

def create_person(db: Session, person: PersonCreate):
    # Converter bytes em imagem OpenCV
    nparr = np.frombuffer(person.image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detecção inicial com YOLOv8
    results = yolo_model(img)
    if not results[0].boxes:  # Nenhum rosto/pessoa detectado
        raise ValueError("Nenhum rosto ou pessoa detectado na imagem.")

    # Gerar embeddings com InsightFace
    faces = face_app.get(img)
    if not faces:
        # Fallback: ReID para tracking de corpo (se rosto não visível)
        # Exemplo com OSNet (adapte conforme necessário)
        raise ValueError("Nenhum rosto detectado, use ReID para tracking.")
    embedding = faces[0].embedding  # Embedding de 512D

    # Salvar no banco
    db_person = PersonModel(
        name=person.name,
        allowed=person.allowed,
        notes=person.notes,
        embedding=embedding.tolist(),
        timestamp=datetime.now(),  # Adicione timestamp
        # camera_id=person.camera_id  # Adicione ID da câmera, se disponível
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

# Função para comparação em tempo real (para detecção)
def compare_embedding(stored_embedding, new_embedding, threshold=0.4):
    similarity = np.dot(stored_embedding, new_embedding) / (np.linalg.norm(stored_embedding) * np.linalg.norm(new_embedding))
    return similarity > threshold  # True = permitida


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
