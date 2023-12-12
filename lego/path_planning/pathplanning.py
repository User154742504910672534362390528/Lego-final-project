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

# Go forward and backwards for one meter.
robot.straight(400)
ev3.speaker.beep()

robot.turn(60)
ev3.speaker.beep()


RECT_X=650
RECT_Y=500

def map_to_rectangle(x,y):
    if x<-RECT_X:
        if y<-RECT_Y:
            return (-RECT_X,-RECT_Y)
        elif y<=RECT_Y:
            return (-RECT_X,y)
        else:
            return (-RECT_X,RECT_Y)
    elif x<=RECT_X:
        if y<-RECT_Y:
            return (x,-RECT_Y)
        elif y<=RECT_Y:
            dist_list=[RECT_X-x,RECT_X+x,RECT_Y-y,RECT_Y+y]
            arg_min=argmin(dist_list)
            if arg_min==0:
                return (RECT_X,y)
            elif arg_min==1:
                return (-RECT_X,y)
            elif arg_min==2:
                return (x,RECT_Y)
            elif arg_min==3:
                return (x,-RECT_Y)
        else:
            return (x,RECT_Y)
    else:
        if y<-RECT_Y:
            return (RECT_X,-RECT_Y)
        elif y<=RECT_Y:
            return (RECT_X,y)
        else:
            return (RECT_X,RECT_Y)

def move_to(curx,cury,cur_angle,destx,desty,dest_angle):
    start_rect=map_to_rectangle(curx,cury)
    end_rect=map_to_rectangle(destx,desty)

def argmin(list):
    min_val=list[0]
    arg_min=0
    for i in range(len(list)):
        if list[i]<min_val:
            arg_min=i
            min_val=list[i]
    return arg_min