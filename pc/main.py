import socket, os, sys
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lego"))

from const import *
from object_recognition import get_ball_pos, get_car_pos
from physics import *

def main():

    # initialize webcam
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
    print("Camera done")
    camera_pos, balls = get_ball_pos(cap)
    print(len(camera_pos))
    print(camera_pos)
    print(balls[-1])
    ret, frame = cap.read()
    small_frame = frame[300:470, 530:810, :]
    for center in camera_pos:
        cx, cy = map(int, center)
        cv2.circle(small_frame, (cx, cy), 8, (255, 0, 0), 2)
    

    final_path = plan_path(balls, HOLES)
    print("final path", final_path)
    final_ball, final_hole = final_path
    print(final_ball.pos, final_hole)

    p1 = np.uint16(real_to_camera(final_ball.pos)[:2])
    p2 = np.uint16(real_to_camera(final_hole)[:2])
    cv2.line(small_frame, p1, p2, (0, 255, 0), 2)
    cv2.imshow("balls", cv2.resize(small_frame, (small_frame.shape[1]*2, small_frame.shape[0]*2)))
    # cv2.waitKey(0)

    # calibrate car
    arucos = get_car_pos(cap)
    for a in arucos:

        cv2.aruco.drawAxis(frame, CAMERA_MTX, np.array([0., 0., 0., 0., 0.]), *a)
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    exit()
    # initialize socket servers
    print("Initializing sockets")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host_ip, PORT))
    server.listen(5)
    print("Server is listening on %s:%d" % (host_ip, PORT))

    client, addr = server.accept()
    print("Client connected " + str(addr))
    client.send("ready".encode())

    while True:
        # wait for client to connect
        try:
            request = client.recv(1024)
            print("Received \"" + request.decode() + "\" from client")
            while 1:
                msg = input("Say something to the client: ")
                if msg == HELP_MSG:
                    continue
                client.send(msg.encode())
                if msg == QUIT_MSG:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            client.close()
            print("Connection closed")
            break
if __name__ == "__main__":
    main()