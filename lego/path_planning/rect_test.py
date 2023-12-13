#!/usr/bin/env pybricks-micropython
from robot_inc import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()
# Initialize the motors.
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=182)

RECT_X=650
RECT_Y=500

def forward(dist):
    robot.straight(-dist)

cur_edge=2
cur_pos=(RECT_X,RECT_Y)
while True:
    if cur_edge==0:
        forward(RECT_X-cur_pos[0])
        cur_pos=(RECT_X,-RECT_Y)
    elif cur_edge==1:
        forward(RECT_Y-cur_pos[1])
        cur_pos=(RECT_X,RECT_Y)
    elif cur_edge==2:
        forward(RECT_X+cur_pos[0])
        cur_pos=(-RECT_X,RECT_Y)
    elif cur_edge==3:
        forward(RECT_Y+cur_pos[1])
        cur_pos=(-RECT_X,-RECT_Y)
    cur_edge=(cur_edge+1)%4
    robot.turn(90)