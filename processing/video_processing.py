from tabnanny import check

import cv2
from ultralytics import YOLO
import yt_dlp
import os
import subprocess

# YOLO model configuration and other parameters
model = YOLO('./models/yolov8n.pt')
classes_of_interest = [0, 2, 5, 7, 9]
class_colors = {                  # Colors are in BGR format
    'person': (255, 0, 0),        # azul
    'car': (0, 255, 0),           # verde
    'bus': (0, 255, 255),         # amarillo
    'truck': (0, 0, 255),         # rojo
    'traffic light': (0, 165, 255)  # naranja
}

def download_video(url, start_time, end_time, output_file):
    # Temporary file name
    temp_file = output_file + "_temp.mp4"

    # Options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[height<=480][fps<=30]/best[height<=480][fps<=30]',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': temp_file,  # Temporary output file name
    }

    try:
        # Download the entire video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Verify if the temporary file was created correctly
        if not os.path.exists(temp_file):
            raise FileNotFoundError(f"Error: The temp file {temp_file} wasn't created")

        # Use ffmpeg to trim the video
        command = [
            'ffmpeg',
            '-i', temp_file,
            '-ss', start_time,
            '-to', end_time,
            '-vf', 'scale=1280:720',
            '-c:v', 'libx264',
            '-crf', '28',
            '-preset', 'fast',
            '-an',  # Remove audio
            output_file
        ]

        subprocess.run(command, check=True)
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading the video: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming the video with ffmpeg: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Delete the temporary file if it exists
        if os.path.exists(temp_file):
            os.remove(temp_file)


def process_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Error opening the video: {video_path}")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detect and track objects
            results = model.track(source=frame, classes=classes_of_interest, conf=0.60, persist=True)

            for result in results[0].boxes:
                box = result.xyxy[0].cpu().numpy()
                label = model.names[int(result.cls[0])]
                confidence = result.conf[0]
                color = class_colors.get(label, (255, 255, 255))

                x1, y1, x2, y2 = box
                label_text = f'{label} {confidence:.2f}'

                # Draw the box and label on the frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                label_y = int(y1) - 10 if int(y1) - 10 > 10 else int(y1) + 10
                cv2.rectangle(frame, (int(x1), label_y - label_size[1] - 10), (int(x1) + label_size[0], label_y + label_size[1] - 10), color, cv2.FILLED)
                cv2.putText(frame, label_text, (int(x1), label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                raise  IOError("Error encoding the frame in JPEG format")

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except IOError as e:
        print(f"IOError: {e}")
    except Exception as e:
        print(f"Unexpected error {e}")
    finally:
        cap.release()
