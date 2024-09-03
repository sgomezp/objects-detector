import os
import requests

MODEL_URL = "URL_DEL_MODELO"
MODEL_PATH = "models/yolov8n.pt"

def download_model():
    if not os.path.exists(MODEL_PATH):
        #print("Downloading model...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, 'wb') as file:
            file.write(response.content)
        #print("Model downloaded.")

# call this function
download_model()
