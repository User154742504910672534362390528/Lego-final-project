from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


ev3 = EV3Brick()
drive_base = DriveBase(Motor(Port.B), Motor(Port.A), 55.5, 104)
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

def parse_command(msg):
    if "turn" in msg:
        msg = msg.split()
        port = get_port(msg[1])
        speed = int(msg[2])
        angle = int(msg[3])
        print(port, speed, angle)
        turn(port, speed, angle)
    elif "beep" in msg:
        beep()
    elif "go" in msg:
        msg = msg.split()
        speed = int(msg[1])
        turn_rate = int(msg[2])
        drive_base.drive(speed, turn_rate)