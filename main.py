from ultralytics import YOLO
import cv2


def main():
    # Load yolov8 model
    model = YOLO('yolov8m.pt')

    classes_of_interest = [0, 2, 5, 7, 9]  # 0 = person, 2 = car, 5 = bus, 7 = truck, 9 = traffic light

    # dictionary that save the color for each label
    class_colors = {'person':(0,0,255),     # blue
                     'car':(0, 255, 0),     # verde
                     'bus':(255, 255, 0),   # Amarillo
                     'truck':(255, 0, 0),   # Naranja
                     'traffic light':(255, 165, 0)  # Rojo
                     }



    # Load video
    video_path = './output_orlando.mp4'
    cap = cv2.VideoCapture(video_path)

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    current_frame = 0
    jump_seconds = 0
    playback_speed = 1  # Normal speed

    # Start playing the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and track objects
        results = model.track(source=frame, classes=classes_of_interest, conf=0.60, persist=True)

        # Iterate over detections to adjust labels manually
        for result in results[0].boxes:
            box = result.xyxy[0].cpu().numpy()
            label = model.names[int(result.cls[0])]  # Class label
            confidence = result.conf[0]  # Confidence score

            # obtaing the class color
            color = class_colors.get(label,(255,255,255))

            # Position the label on the top-left corner of the box
            x1, y1, x2, y2 = box
            label_text = f'{label} {confidence:.2f}'

            # Draw the box with the corresponding color


            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

            # Draw the label, adjusting position to avoid overlap
            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            label_y = int(y1) - 10 if int(y1) - 10 > 10 else int(y1) + 10
            cv2.rectangle(
                frame, (int(x1), label_y - label_size[1] - 10), (int(x1) + label_size[0], label_y + label_size[1] - 10),
                (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, label_text, (int(x1), label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow('frame', frame)

        key = cv2.waitKey(int(1000 / (frame_rate * playback_speed)))  # Wait and check key press
        if key == ord('q'):  # Exit if 'q' is pressed
            break
        elif key == ord('j'):  # Jump forward
            jump_seconds = int(input("Enter number of seconds to jump forward: "))
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + jump_seconds * 1000)
        elif key == ord('k'):  # Jump backward
            jump_seconds = int(input("Enter number of seconds to jump backward: "))
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) - jump_seconds * 1000)
        elif key == ord('f'):  # Fast forward (speed up)
            playback_speed = min(playback_speed + 0.5, 4)  # Cap speed to 4x
        elif key == ord('s'):  # Slow down
            playback_speed = max(playback_speed - 0.5, 0.5)  # Cap speed to 0.5x

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
