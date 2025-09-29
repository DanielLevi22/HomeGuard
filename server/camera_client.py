import cv2
import requests
import time
import os

API_URL = "http://127.0.0.1:8000/check/"  # Ajuste para sua API
SAVE_DEBUG = True  # Ativar salvar frames em disco
DEBUG_DIR = "debug_frames"

if SAVE_DEBUG and not os.path.exists(DEBUG_DIR):
    os.makedirs(DEBUG_DIR)

# Inicializa câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: câmera não encontrada.")
    exit()

print("Câmera iniciada. Pressione CTRL+C para parar.")

frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Erro ao capturar frame.")
            time.sleep(1)
            continue

        frame_count += 1

        # Salva o frame em disco para debug
        if SAVE_DEBUG:
            frame_path = os.path.join(DEBUG_DIR, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Frame salvo: {frame_path}")

        # Converte frame para JPEG
        _, img_encoded = cv2.imencode(".jpg", frame)
        files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}

        try:
            response = requests.post(API_URL, files=files, data={"test_mode": True})
            print("Resposta da API:", response.json())
        except Exception as e:
            print("Erro ao enviar para API:", e)

        time.sleep(3)  # Intervalo entre capturas

except KeyboardInterrupt:
    print("Encerrando captura...")

finally:
    cap.release()
    cv2.destroyAllWindows()
