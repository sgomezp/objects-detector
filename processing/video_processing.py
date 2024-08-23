import cv2
from ultralytics import YOLO
import yt_dlp
import os
import subprocess

# Configuración del modelo YOLO y otros parámetros
model = YOLO('yolov8n.pt')
classes_of_interest = [0, 2, 5, 7, 9]
class_colors = {                  # Colors are in BGR format
    'person': (255, 0, 0),        # azul
    'car': (0, 255, 0),           # verde
    'bus': (0, 255, 255),         # amarillo
    'truck': (0, 0, 255),         # rojo
    'traffic light': (0, 165, 255)  # naranja
}

def download_video(url, start_time, end_time, output_file):
    # Nombre del archivo temporal
    temp_file = output_file + "_temp.mp4"

    # Opciones para yt-dlp
    ydl_opts = {
        'format': 'bestvideo[height<=480][fps<=30]/best[height<=480][fps<=30]',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': temp_file,  # Nombre del archivo de salida temporal
    }

    # Descargar el video completo
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Verificar si el archivo temporal fue creado correctamente
    if not os.path.exists(temp_file):
        print(f"Error: El archivo temporal {temp_file} no fue creado.")
        return

    # Usar ffmpeg para recortar el video
    command = [
        'ffmpeg',
        '-i', temp_file,
        '-ss', start_time,
        '-to', end_time,
        '-vf', 'scale=1280:720',
        '-c:v', 'libx264',
        '-crf', '28',
        '-preset', 'fast',
        '-an',  # Eliminar el audio
        output_file
    ]

    subprocess.run(command)

    # Eliminar el archivo temporal
    os.remove(temp_file)


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar y rastrear objetos
        results = model.track(source=frame, classes=classes_of_interest, conf=0.60, persist=True)

        for result in results[0].boxes:
            box = result.xyxy[0].cpu().numpy()
            label = model.names[int(result.cls[0])]
            confidence = result.conf[0]
            color = class_colors.get(label, (255, 255, 255))

            x1, y1, x2, y2 = box
            label_text = f'{label} {confidence:.2f}'

            # Dibujar la caja y la etiqueta en el frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            label_y = int(y1) - 10 if int(y1) - 10 > 10 else int(y1) + 10
            cv2.rectangle(frame, (int(x1), label_y - label_size[1] - 10), (int(x1) + label_size[0], label_y + label_size[1] - 10), color, cv2.FILLED)
            cv2.putText(frame, label_text, (int(x1), label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Codificar el frame para la transmisión
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
