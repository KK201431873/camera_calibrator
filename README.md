# camera_calibrator

Get camera intrinsics using opencv. Below is how to use.


## Taking pictures

Run `take_pictures.py` and take pictures of ChAruCo boards. If it doesn't run, change the camera index on this line: 

    cap = cv2.VideoCapture(4, cv2.CAP_V4L2)

The images are saved to `calib_images/`


## Calibration

Run `calib_aruco.py`, if every image fails, change the params on these lines:

    rows = 8
    cols = 11
    square_length = 0.020   # 20 mm → meters
    marker_length = 0.015   # 15 mm → meters

## Note

I did this on Linux Mint so code might not work first try for other OS.