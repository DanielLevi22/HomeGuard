from fastapi  import FastAPI
from api.v1 import person
from core.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="HomeGuard", description="Sistema de reconhecimento facial e detecção de pessoas", version="0.1.0")


app.include_router(person.router)



@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    main()
