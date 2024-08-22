from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Configura tu modelo YOLO
model = YOLO('yolov8m.pt')
classes_of_interest = [0, 2, 5, 7, 9]
class_colors = {
    'person': (255, 0, 0),        # azul
    'car': (0, 255, 0),           # verde
    'bus': (0, 255, 255),         # amarillo
    'truck': (0, 0, 255),         # rojo
    'traffic light': (0, 165, 255)  # naranja
}

def process_video():
    video_path = './static/output_orlando.mp4'
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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
