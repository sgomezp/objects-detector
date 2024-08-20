from ultralytics import YOLO
import cv2


# Load yolov8 model
model = YOLO('yolov8n.pt')

classes_of_interest = [0,16] # 0 = persons 16 = dogs

# load video
video_path = './test.mp4'
cap = cv2.VideoCapture(video_path)

ret = True
# read frames
while ret:
    ret, frame = cap.read()

    if ret:
        # detect and track objects
        results = model.track(source=frame, classes=classes_of_interest,persist=True)

        # plot results
        frame_ = results[0].plot()

        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()



