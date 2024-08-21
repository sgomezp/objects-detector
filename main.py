from ultralytics import YOLO
import cv2


# Load yolov8 model
model = YOLO('yolov8m.pt')

classes_of_interest = [0,2,5,7,9] # 0 = person, 2 = car 5 = bus,  7= truck, 8= traffic light

# dictionary that save the color for each label
class_colors = {'person':(0,0,255),     # blue
                 'car':(0, 255, 0),     # verde
                 'bus':(255, 255, 0),   # Amarillo
                 'truck':(255, 0, 0),   # Naranja
                 'traffic light':(255, 165, 0)  # Rojo
                 }


# load video
video_path = './output_orlando.mp4'
cap = cv2.VideoCapture(video_path)

ret = True
# read frames
while ret:
    ret, frame = cap.read()

    if ret:
        # detect and track objects
        results = model.track(source=frame, classes=classes_of_interest,conf= 0.60, persist=True)

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

        # plot results
        #frame_ = results[0].plot()

        # visualize
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()



