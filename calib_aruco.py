import os
import cv2
import glob
import numpy as np

# ---------- Board definition ----------
image_folder = "./calib_images"  # folder with your images
rows = 8
cols = 11
square_length = 0.020   # 20 mm → meters
marker_length = 0.015   # 15 mm → meters

aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

board = cv2.aruco.CharucoBoard(
    (cols, rows),
    square_length,
    marker_length,
    aruco_dict
)


# ---------- Load images ----------
image_paths = sorted(glob.glob(os.path.join(image_folder, "*.png")))
assert len(image_paths) > 10, "Not enough images"

all_detected_xy = []

all_corners = []
all_ids = []
image_size = None

# ---------- Detect markers ----------
charuco_detector = cv2.aruco.CharucoDetector(board)

for path in image_paths:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if image_size is None:
        image_size = gray.shape[::-1]

    charuco_corners, charuco_ids, _, _ = charuco_detector.detectBoard(gray)

    if charuco_ids is not None and len(charuco_ids) > 0:
        all_corners.append(charuco_corners)
        all_ids.append(charuco_ids)

        # charuco_corners shape: (N, 1, 2)
        all_detected_xy.append(charuco_corners.reshape(-1, 2))
        print(f"good image {path}")
    else:
        print(f"bad image {path}")

print(f"Usable frames: {len(all_corners)}")

# ---------- Calibrate ----------
ret, K, D, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
    all_corners,
    all_ids,
    board,
    image_size,
    None,
    None
)

print("Reprojection error:", ret)
print("Camera matrix:\n", K)
print("Distortion coefficients:\n", D)

# corner coverage
import matplotlib.pyplot as plt
import numpy as np

# Stack all points
pts = np.vstack(all_detected_xy)

w, h = image_size  # image_size was set earlier as (width, height)

plt.figure(figsize=(6, 4))
plt.scatter(pts[:, 0], pts[:, 1], s=2, alpha=0.4)
plt.title("Charuco Corner Coverage")
plt.xlabel("x (pixels)")
plt.ylabel("y (pixels)")
plt.xlim(0, w)
plt.ylim(h, 0)   # invert y-axis to match image coordinates
plt.gca().set_aspect("equal", adjustable="box")
plt.grid(True)
plt.show()
