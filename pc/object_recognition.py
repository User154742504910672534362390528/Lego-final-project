import cv2
import numpy as np
from copy import deepcopy
from physics import *

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
hmin = hmax = smin = smax = vmin = vmax = 0
hmin = 7
hmax = 7
vmin = 40
vmax = 14
smin = 20
smax = 31


# CAMERA_MTX = np.array(
#     [
#         [650.59819165, 0.        ,317.94835167],
#         [  0.        ,653.61004762 ,242.65273137],
#         [  0.          ,0.          ,1.        ]
#     ]
# )



kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CIRCLE_RADIUS, CIRCLE_RADIUS))
# kernel = 1-kernel
kernel = kernel|kernel.T
# # kernel = np.array(
# #     [
# #         [0, 1, 1, 1, 0],
# #         [1, 1, 1, 1, 1],
# #         [1, 1, 1, 1, 1],
# #         [1, 1, 1, 1, 1],
# #         [0, 1, 1, 1, 0],
# #     ], dtype=np.uint8
# # )
'''
while 1:
    ret, frame = cap.read()
    print(frame.shape)
    width, height = frame.shape[:2]
    # logi camera
    # 480, 640
    # WXL phone
    # 720 1080
    # print(width, height)
    cv2.imshow("og frame", frame)
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = frame[300:470, 530:810, :]
    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (9, 9), 0), cv2.COLOR_BGR2HSV)
    # print(hsv[frame.shape[0]//2, frame.shape[1]//2])
    data = hsv[frame.shape[0]//2, frame.shape[1]//2]
    # high = np.array([hmax, smax, vmax])
    # low = np.array([hmin, smin, vmin])
    # high = np.array([data[0] + h, data[1] + s, data[2] + v])
    # low = np.array([data[0] - h, data[1] - s, data[2] - v])
    high = np.array([data[0] + hmax, data[1] + smax, data[2] + vmax])
    low = np.array([data[0] - hmin, data[1] - smin, data[2] - vmin])
    filter_hsv = cv2.inRange(hsv, low, high)
    cv2.imshow("hsv", filter_hsv)
    neg = cv2.bitwise_not(filter_hsv)

    cv2.imshow("neg", neg)

    closed_hsv = cv2.dilate(neg, kernel)
    closed_hsv = cv2.erode(closed_hsv, kernel)
    
    cv2.imshow("morph", closed_hsv)
    closed_hsv = cv2.bitwise_not(closed_hsv)
    # closed_hsv = cv2.(closed_hsv, kernel)
    all_circles = []
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=15, minRadius=15, maxRadius=25)
    circles = cv2.HoughCircles(filter_hsv, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=9, minRadius=5, maxRadius=10)
    # circles = cv2.HoughCircles(filter_hsv, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=15, minRadius=15, maxRadius=25)
    if circles is not None:
        # count -= 1
        circles = np.uint16(np.around(circles))
        all_circles.append(circles)
        for c in circles[0, :]:
            cv2.circle(frame, (c[0], c[1]), c[2], (255, 255, 255), 2)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # # canny = cv2.Canny(blur, 50, 100)
    # ret, canny = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)
    # cv2.imshow('canny', canny)
    # contours, hie = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # # print(len(contours))
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     # print(area, end=" ")
    #     if area < 100:
    #         continue
    #     M = cv2.moments(cnt)

    #     # cx = int(M["m10"]/M["m00"])
    #     # cy = int(M["m01"]/M["m00"])
    #     # rect = cv2.minAreaRect(cnt)
    #     # box = cv2.boxPoints(rect)
    #     # box = np.int0(box)
    #     # rect = cv2.boundingRect(cnt)
    #     # cv2.rectangle(frame, *rect)
    #     cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
    # print()
    # cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 10, (0, 0, 255), 1)
    cv2.circle(frame, list(map(int, real_to_camera((0, 0))[:2])), 10, (255, 0, 0), 2)
    cv2.circle(frame, list(map(int, real_to_camera(HOLES[0])[:2])), 10, (255, 0, 0), 2)
    cv2.circle(frame, list(map(int, real_to_camera(HOLES[1])[:2])), 10, (255, 0, 0), 2)
    cv2.circle(frame, list(map(int, real_to_camera(HOLES[2])[:2])), 10, (255, 0, 0), 2)
    cv2.circle(frame, list(map(int, real_to_camera(HOLES[3])[:2])), 10, (255, 0, 0), 2)
    cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 10, (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    # if key == ord("q"):
    #     break
    # elif key == ord('6'):
    #     thresh += 1
    #     print(thresh)
    # elif key == ord('4'):
    #     thresh -= 1
    #     print(thresh)
    # elif key == ord('h'):
    #     h += 1
    #     print(h, s, v)
    # elif key == ord('g'):
    #     h -= 1
    #     print(h, s, v)
    # elif key == ord('s'):
    #     s += 1
    #     print(h, s, v)
    # elif key == ord('a'):
    #     s -= 1
    #     print(h, s, v)
    # elif key == ord('v'):
    #     v += 1
    #     print(h, s, v)
    # elif key == ord('c'):
    #     v -= 1
    #     print(h, s, v)
    # elif key == ord('r'):
    #     h, s, v = 11, 73, 32
    #     print(h, s, v)
    if key == ord("q"):
        break
    elif key == ord('h'):
        hmax += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('g'):
        hmin += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('s'):
        smax += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('a'):
        smin += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('v'):
        vmax += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('c'):
        vmin += 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('H'):
        hmax -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('G'):
        hmin -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('S'):
        smax -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('A'):
        smin -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('V'):
        vmax -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('C'):
        vmin -= 1
        print(hmin, hmax, vmin, vmax, smin, smax)
    elif key == ord('r'):
        hmin=hmax=vmin=vmax=smin=smax = 0
        print(hmin, hmax, vmin, vmax, smin, smax)
    
    

cap.release()
cv2.destroyAllWindows()
#'''


def dist(p1, p2):
    return np.linalg.norm(p1 - p2)
    # print(p1, p2)
    # print(np.dtype(p1[0]), np.dtype(p2[0]))
    # return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class Tracker:
    def __init__(self, missing_frames=50, max_displacement=25) -> None:
        self.next_id = 0
        self.objects = {}
        self.trajectory = {}
        self.disappeared = {}
        
        self.max_missing_frames = missing_frames
        self.max_displacement = max_displacement

    def new_obj(self, pos):
        self.objects[self.next_id] = pos
        self.trajectory[self.next_id] = [pos, ]
        self.disappeared[self.next_id] = 0

        self.next_id += 1

    def delete_obj(self, id):
        # print("deleta")
        self.objects.pop(id)
        self.trajectory.pop(id)
        self.disappeared.pop(id)

    def update_obj(self, circles):
        # print("obj", circles)
        if len(circles) == 0:
            # nothing to track, mark everything as gone
            for id in list(self.disappeared.keys()):
                self.disappeared[id] += 1

                if self.disappeared[id] > self.max_missing_frames:
                    self.delete_obj(id)

        else:
            if len(self.objects) == 0:
                # currently not tracking anything
                for circle in circles:
                    center = circle[:2]
                    self.new_obj(center)

            else:
                distance_array = []
                for obj in self.objects.values():
                    tmp = []
                    for circle in circles:
                        center = circle[:2]
                        tmp.append(dist(center, obj))
                    distance_array.append(tmp)
                distance_array = np.array(distance_array)

                rows = distance_array.min(axis=1).argsort()
                cols = distance_array.argmin(axis=1)[rows]

                used_row, used_col = set(), set()

                unused_row = set(range(distance_array.shape[0])).difference(used_row)
                unused_col = set(range(distance_array.shape[1])).difference(used_col)
                # print(distance_array)
                while 1:
                    rows = distance_array.min(axis=1).argsort()
                    cols = distance_array.argmin(axis=1)[rows]

                    tmp = []

                    for row, col in zip(rows, cols):
                        if row in used_row or col in used_col:
                            continue
                        tmp.append((row, col))

                    for row, col in tmp:
                        if distance_array[row, col] <= self.max_displacement:
                            obj_id = list(self.objects.keys())[row]

                            self.objects[obj_id] = circles[col][:2]
                            self.trajectory[obj_id].append(circles[col][:2])
                            self.disappeared[obj_id] = 0

                            used_row.add(row)
                            used_col.add(col)

                            unused_row.remove(row)
                            unused_col.remove(col)

                            distance_array[row] = 999999999
                            distance_array[:, col] = 999999999
                            break
                    else:
                        break

                keys = deepcopy(self.objects).keys()
                # print("uur, uuc", unused_row, unused_col)
                for row in unused_row:
                    obj_id = list(keys)[row]

                    self.disappeared[obj_id] += 1

                    if self.disappeared[obj_id] > self.max_missing_frames:
                        self.delete_obj(obj_id)
                for col in unused_col:
                    # print("COL", circles[col])
                    self.new_obj(circles[col][:2])

def get_car_pos(cap):
    ret, frame = cap.read()
    
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    marker_corners, marker_ids, rej = cv2.aruco.detectMarkers(frame, arucoDict)

    if marker_ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_ids)
        rv, tv, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, 35, CAMERA_MTX, np.array([0., 0., 0., 0., 0.]))
        
        for i in range(len(marker_ids)):
            cv2.aruco.drawAxis(frame, CAMERA_MTX, np.array([0., 0., 0., 0., 0.]), rv[i], tv[i], 35)
            cx = int(np.mean(marker_corners[i][0][:, 0]))
            cy = int(np.mean(marker_corners[i][0][:, 1]))

            print(cx, cy, i, marker_ids[i], np.degrees(rv[i]))
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

    return


def get_ball_pos(cap):
    '''
    return a list of coordinates of balls
    '''
    count = 50
    min_frames = 10
    # take some frames and average them to prevent noise
    all_circles = []
    while count > 0:
        ret, frame = cap.read()
        # cv2.imshow("frame", frame)
        width, height = frame.shape[:2]
        frame = frame[300:470, 530:810, :]
        cv2.imshow("frm", frame)
        # cv2.waitKey(0)
        hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (9, 9), 0), cv2.COLOR_BGR2HSV)
        data = hsv[frame.shape[0]//2, frame.shape[1]//2]
        high = np.array([data[0] + hmax, data[1] + smax, data[2] + vmax])
        low = np.array([data[0] - hmin, data[1] - smin, data[2] - vmin])
        filter_hsv = cv2.inRange(hsv, low, high)

        neg = cv2.bitwise_not(filter_hsv)
        closed_hsv = cv2.dilate(neg, kernel)
        closed_hsv = cv2.erode(closed_hsv, kernel)

        closed_positive = cv2.bitwise_not(closed_hsv)

        circles = cv2.HoughCircles(filter_hsv, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=9, minRadius=5, maxRadius=10)
        # circles = cv2.HoughCircles(filter_hsv, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=15, minRadius=15, maxRadius=25)
        # circles = cv2.HoughCircles(closed_positive, cv2.HOUGH_GRADIENT, 1, 15, param1=30, param2=15, minRadius=15, maxRadius=25)
        if circles is not None:
            count -= 1
            print(count)
            # circles = np.uint16(np.around(circles))
            circles = np.around(circles)
            all_circles.append(circles[0, :])
            # for c in circles[0, :]:
            #     cv2.circle(frame, (c[0], c[1]), c[2], (255, 255, 255), 1)

        # cv2.imshow("frame", frame)
        # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    tracker = Tracker()
    # print(all_circles)
    for round in all_circles:
        # print("round", r:=len(round))
        tracker.update_obj(round)
        # print("track", t:=len(tracker.objects))
        # if t > r:
        #     print(round)
        #     print(tracker.objects)
            # exit()

    centers = []
    balls = []
    # print(centers)
    for key, trajectory in tracker.trajectory.items():
        # print(trajectory)
        # if len(trajectory) < min_frames:
        #     continue
        array = np.array(trajectory, dtype=np.float32)
        average_center = np.sum(array, axis=0) / len(trajectory)
        centers.append(average_center)
        balls.append(Ball(transform(average_center)[1::-1], key))
        # trans = transform(average_center)
        # print(average_center, trans[1::-1])
        # centers.append(trans[1::-1])

    return centers, balls