import cv2
import numpy as np
from physics import *
print(cv2.__version__)

def my_estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    '''
    This will estimate the rvec and tvec for each of the marker corners detected by:
       corners, ids, rejectedImgPoints = detector.detectMarkers(image)
    corners - is an array of detected corners for each detected marker in the image
    marker_size - is the size of the detected markers
    mtx - is the camera matrix
    distortion - is the camera distortion matrix
    RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
    '''
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash

try:
    print("Initializing camera")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    if not cap.isOpened():
        print("camera off")
        exit(1)
except Exception as e:
    print(e)
    exit(1)

ret, frame = cap.read()
image = frame
# print(aruco.Dictionary)
# cv2.arucoDict(cv2.aruco.DICT_4X4_50)
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_corners, marker_ids, rej = cv2.aruco.detectMarkers(frame, arucoDict)
# arucoParams = cv2.aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(arucoDict,arucoParams)

# marker_corners, marker_ids, rej = detector.detectMarkers(image)


# print(marker_corners)
# print(marker_ids)
# print(rej)

if marker_ids is not None:
    cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_ids)
    # rv, tv, _ = my_estimatePoseSingleMarkers(marker_corners, 50, CAMERA_MTX, np.array([0, 0, 0, 0, 0]))
    rv, tv, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, 35, CAMERA_MTX, np.array([0, 0, 0, 0, 0]))
    

    for i in range(len(marker_ids)):
        cv2.aruco.drawAxis(frame, CAMERA_MTX, np.array([0., 0., 0., 0., 0.]), rv[i], tv[i], 100)
        cx = int(np.mean(marker_corners[i][0][:, 0]))
        cy = int(np.mean(marker_corners[i][0][:, 1]))

        print(cx, cy, i, marker_ids[i], np.degrees(rv[i]))
cv2.imshow("frame", frame)
cv2.waitKey(0)

cap.release()