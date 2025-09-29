import cv2
import numpy as np
from datetime import datetime
from insightface.app import FaceAnalysis
from ultralytics import YOLO
from sqlalchemy.orm import Session
from models.person import Person as PersonModel
from schemas.person import PersonCreate
from huggingface_hub import hf_hub_download
import onnxruntime as ort
from fastapi import HTTPException

# -----------------------------
# Carregar modelo YOLOv8
# -----------------------------
model_path = hf_hub_download(
    repo_id="arnabdhar/YOLOv8-Face-Detection",
    filename="model.pt"
)
yolo_model = YOLO(model_path)

# -----------------------------
# Inicializar InsightFace
# -----------------------------
face_app = FaceAnalysis(providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

# -----------------------------
# Carregar modelo anti-spoofing ONNX
# -----------------------------
anti_spoof_session = ort.InferenceSession("models/anti_spoof.onnx")

# -----------------------------
# Função de anti-spoofing
# -----------------------------
def check_antispoof(img, threshold: float = 0.5):
    """
    Retorna 1 se for rosto real, 0 se spoof.
    O modelo retorna probabilidade/logits -> usamos argmax ou threshold.
    """
    img_input = cv2.resize(img, (112, 112))
    img_input = img_input.transpose(2, 0, 1).astype(np.float32) / 255.0
    img_input = img_input[np.newaxis, ...]

    input_name = anti_spoof_session.get_inputs()[0].name
    outputs = anti_spoof_session.run(None, {input_name: img_input})

    # outputs[0] pode ser [prob_spoof, prob_real]
    probs = outputs[0].squeeze()
    if probs.ndim == 1 and len(probs) == 2:
        score_real = float(probs[1])  # probabilidade de real
        print(f"[ANTI-SPOOF] Score real={score_real:.4f}")
        return 1 if score_real >= threshold else 0
    else:
        # fallback: classificação direta
        pred_label = int(np.argmax(outputs[0]))
        print(f"[ANTI-SPOOF] Pred_label={pred_label}")
        return pred_label


# -----------------------------
# CRUD e funções principais
# -----------------------------
def create_person(db: Session, person: PersonCreate):
    nparr = np.frombuffer(person.image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Anti-spoofing
    if check_antispoof(img) == 0:
        raise HTTPException(status_code=400, detail="Spoofing detectado!")

    # Detecção com YOLOv8
    results = yolo_model(img)
    if not results[0].boxes:
        raise ValueError("Nenhum rosto detectado na imagem.")

    # InsightFace embeddings
    faces = face_app.get(img)
    if not faces:
        raise ValueError("Nenhum rosto detectado para embedding.")
    embedding = faces[0].embedding

    db_person = PersonModel(
        name=person.name,
        allowed=person.allowed,
        notes=person.notes,
        embedding=embedding.tolist(),
        timestamp=datetime.now()
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


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


# -----------------------------
# Classificação de pessoa
# -----------------------------
def classify_person(file, db):
    img_bytes = file.file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    print("[DEBUG] Imagem carregada:", img.shape if img is not None else "Erro")

    # Anti-spoofing
    spoof_check = check_antispoof(img)
    print(f"[DEBUG] Resultado anti-spoof: {spoof_check}")
    if spoof_check == 0:
        raise HTTPException(status_code=400, detail="Spoofing detectado!")

    # Detecção de rosto
    results = yolo_model(img)
    print(f"[DEBUG] YOLOv8 detectou {len(results[0].boxes)} rostos")
    if not results[0].boxes:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado!")

    # InsightFace embeddings
    faces = face_app.get(img)
    print(f"[DEBUG] InsightFace detectou {len(faces)} rostos")
    if not faces:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado para embedding!")

    embedding = faces[0].embedding

    # Comparar com embeddings existentes
    existing_people = get_all_person_embeddings(db)
    print(f"[DEBUG] Banco contém {len(existing_people)} pessoas")

    def cosine_similarity(a, b):
        from numpy import dot
        from numpy.linalg import norm
        return dot(a, b) / (norm(a) * norm(b))

    for person in existing_people:
        sim = cosine_similarity(embedding, np.array(person['embedding']))
        print(f"[DEBUG] Comparando com {person['name']} -> sim={sim:.4f}")
        if sim > 0.7:
            return {
                "recognized": True,
                "name": person['name'],
                "allowed": person['allowed'],
                "similarity": sim
            }

    return {"recognized": False}



def get_all_person_embeddings(db: Session):
    """
    Retorna todos os embeddings cadastrados no banco
    em formato de lista de dicionários {name, allowed, embedding}.
    """
    people = db.query(PersonModel).all()
    return [
        {
            "name": p.name,
            "allowed": p.allowed,
            "embedding": p.embedding
        }
        for p in people
    ]
