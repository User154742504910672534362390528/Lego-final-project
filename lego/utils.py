from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
# import os, sys
# sys.path.append("../" )
import HitBall
from HitBall import parameters

ev3 = EV3Brick()
drive_base = DriveBase(Motor(Port.B), Motor(Port.A), parameters.WHEEL_DIAMETER, parameters.AXLE_TRACK)

def beep():
    ev3.speaker.beep()

def turn(port=Port.A, speed=1000, angle=3600):
    test_motor = Motor(port)
    test_motor.run_target(speed, angle)

def get_port(port_str):
    if port_str  == "A":
        return Port.A
    if port_str  == "B":
        return Port.B
    if port_str  == "C":
        return Port.C
    if port_str  == "D":
        return Port.D

def fire(port=Port.A, speed=1000, angle=-150):
    fire_motor = Motor(port)
    fire_motor.run_target(speed, angle)
    time.sleep(2)
    fire_motor.run_target(speed/2, -angle)

def parse_command(msg: str):
    if "turn" in msg:
        msg = msg.split()
        port = get_port(msg[1])
        speed = int(msg[2])
        angle = int(msg[3])
        print(port, speed, angle)
        turn(port, speed, angle)
    elif "beep" in msg:
        beep()
    elif "fire" in msg:
        msg = msg.split()
        port = get_port(msg[1])
        fire(port)
    elif "go" in msg:
        msg = msg.split()
        speed = int(msg[1])
        turn_rate = int(msg[2])
        drive_base.drive(speed, turn_rate)
    elif "hit" in msg:
        msg = msg.split()
        x = int(msg[1])
        y = int(msg[2])
        longtitude = int(msg[3])
        latitude = int(msg[4])
        HitBall.HitBall(x, y, longtitude, latitude)
    elif "path" in msg:
        msg = msg.split()
        curx =int(msg[1])
        cury =int(msg[2])
        cur_angle =int(msg[3])
        destx =int(msg[4])
        desty =int(msg[5])
        dest_angle =int(msg[6])
        HitBall.path_planning(curx,cury,cur_angle,destx,desty,dest_angle)