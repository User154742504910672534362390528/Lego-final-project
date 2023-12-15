import numpy as np
import cv2

from numpy.linalg import inv

# IMG_NUM = 10

def calibrate(imgs):
    print("start calibrate:")
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((8*6,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images=imgs
    img_size=(0,0)
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_size=gray.shape[::-1]
        print(img_size)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (8, 6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            print("True")
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    return mtx
    
CAMERA_MTX= calibrate() #get this from calibrate camera
camera_mtx_inv=inv(CAMERA_MTX) # invesing the matrix is required (see the definition of camera matrix)


def main():
    try:
        print(1)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # cap.set(cv2.CAP_PROP_SETTINGS, 1)
        print(2)
        if not cap.isOpened():
            print("exit")
            exit(0)
    except Exception as e:
        print(e)
        exit()
    images = []
    while 1:
        ret, frame = cap.read()
        cv2.imshow("press C to calibrate", frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break
        elif key == ord("c"):
            images.append(frame)
            calibrate(images)

if __name__ == "__main__":
    main()