import cv2
import numpy as np

try:
    print(1)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
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



small_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (OPEN_RADIUS, OPEN_RADIUS))
small_kernel = small_kernel | small_kernel.T
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CIRCLE_RADIUS, CIRCLE_RADIUS))
# kernel = 1-kernel
kernel = kernel|kernel.T
# kernel = np.array(
#     [
#         [0, 1, 1, 1, 0],
#         [1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1],
#         [0, 1, 1, 1, 0],
#     ], dtype=np.uint8
# )

while 1:
    ret, frame = cap.read()
    width, height = frame.shape[:2]
    # 480, 640
    # print(width, height)
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

    closed_hsv = cv2.dilate(neg, kernel)
    closed_hsv = cv2.erode(closed_hsv, kernel)
    
    cv2.imshow("morph", closed_hsv)
    closed_hsv = cv2.bitwise_not(closed_hsv)
    # closed_hsv = cv2.(closed_hsv, kernel)
    contours, hie = cv2.findContours(closed_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    for cnt in contours:
        # area = cv2.contourArea(cnt)
        # if area < AREA_THRESH_MIN or area > AREA_THRESH_MAX:
        #     continue
        # M = cv2.moments(cnt)
        # cx = int(M["m10"]/M["m00"])
        # cy = int(M["m01"]/M["m00"])
        # cv2.circle(frame, (cx, cy), CIRCLE_RADIUS, (0, 255, 0), 1)

        coordiniate = []
        approx = cv2.approxPolyDP(cnt, 0.07 * cv2.arcLength(cnt, True), True)
        if (len(approx) == 3):
            coordiniate.append([cnt])

    kpCnt = len(coordiniate)
    x = 0
    y = 0

    for kp in coordiniate:
        x = x+kp[0][0]
        y = y+kp[0][1]

    print(np.uint8(np.ceil(x/kpCnt)), np.uint8(np.ceil(y/kpCnt)))
    
    

cap.release()
cv2.destroyAllWindows()