import cv2
import numpy as np

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

thresh = 156
h = 11
s = 73
v = 32
AREA_THRESH_MIN = 60
AREA_THRESH_MAX = 500
CIRCLE_RADIUS = 10
OPEN_RADIUS = 9

while 1:
    ret, frame = cap.read()
    width, height = frame.shape[:2]
    # 480, 640
    print(width, height)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (9, 9), 0), cv2.COLOR_BGR2HSV)
    # print(hsv[frame.shape[0]//2, frame.shape[1]//2])
    data = hsv[frame.shape[0]//2, frame.shape[1]//2]
    high = np.array([data[0] + h, data[1] + s, data[2] + v])
    low = np.array([data[0] - h, data[1] - s, data[2] - v])
    filter_hsv = cv2.inRange(hsv, low, high)
    cv2.imshow("hsv", filter_hsv)
    neg = cv2.bitwise_not(filter_hsv)
    cv2.imshow("neg", neg)
    circles = cv2.HoughCircles(neg, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=15, minRadius=15, maxRadius=25)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(circles)
        for c in circles[0, :]:
            cv2.circle(frame, (c[0], c[1]), c[2], (255, 255, 255), 1)
    
    cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 10, (0, 0, 255), 1)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        input("break")
        break
    elif key == ord('6'):
        thresh += 1
        print(thresh)
    elif key == ord('4'):
        thresh -= 1
        print(thresh)
    elif key == ord('h'):
        h += 1
        print(h, s, v)
    elif key == ord('g'):
        h -= 1
        print(h, s, v)
    elif key == ord('s'):
        s += 1
        print(h, s, v)
    elif key == ord('a'):
        s -= 1
        print(h, s, v)
    elif key == ord('v'):
        v += 1
        print(h, s, v)
    elif key == ord('c'):
        v -= 1
        print(h, s, v)
    elif key == ord('r'):
        h, s, v = 11, 73, 32
        print(h, s, v)
    
    

cap.release()
cv2.destroyAllWindows()