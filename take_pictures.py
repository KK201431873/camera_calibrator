import os
import cv2
import time

save_dir = "calib_images"
os.makedirs(save_dir, exist_ok=True)

# Change the number to your camera index (0, 1, 2...) 
# or use /dev/videoX as the index if needed
cap = cv2.VideoCapture(4, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
cap.set(cv2.CAP_PROP_FPS, 10)

# Attempt to disable auto exposure and set manual exposure (driver dependent)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)   # 1 = manual mode for v4l2 backend
cap.set(cv2.CAP_PROP_EXPOSURE, 10)      # value in ms
cap.set(cv2.CAP_PROP_GAIN, 0)           # adjust as needed

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Preview", frame)

    key = cv2.waitKey(1)
    if key == ord('c'):  # press 'c' to capture
        filename = os.path.join(save_dir, f"capture_{int(time.time())}.png")
        cv2.imwrite(filename, frame)
        print("Saved", filename)
    elif key == ord('q'):  # press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
