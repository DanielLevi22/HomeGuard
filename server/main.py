from fastapi import FastAPI

app = FastAPI(title="HomeGuard", description="Sistema de reconhecimento facial e detecção de pessoas", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello World"}




def main():
    print("Hello from server!")


if __name__ == "__main__":
    main()
