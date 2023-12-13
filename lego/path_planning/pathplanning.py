#!/usr/bin/env pybricks-micropython
from robot_inc import *
import numpy as np

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
# robot.straight(400)
# ev3.speaker.beep()

# robot.turn(3600)
# ev3.speaker.beep()


RECT_X=650
RECT_Y=500

# def map_to_rectangle(x,y):
#     if x<-RECT_X:
#         if y<-RECT_Y:
#             return (-RECT_X,-RECT_Y)
#         elif y<=RECT_Y:
#             return (-RECT_X,y)
#         else:
#             return (-RECT_X,RECT_Y)
#     elif x<=RECT_X:
#         if y<-RECT_Y:
#             return (x,-RECT_Y)
#         elif y<=RECT_Y:
#             dist_list=[RECT_X-x,RECT_X+x,RECT_Y-y,RECT_Y+y]
#             arg_min=argmin(dist_list)
#             if arg_min==0:
#                 return (RECT_X,y)
#             elif arg_min==1:
#                 return (-RECT_X,y)
#             elif arg_min==2:
#                 return (x,RECT_Y)
#             elif arg_min==3:
#                 return (x,-RECT_Y)
#         else:
#             return (x,RECT_Y)
#     else:
#         if y<-RECT_Y:
#             return (RECT_X,-RECT_Y)
#         elif y<=RECT_Y:
#             return (RECT_X,y)
#         else:
#             return (RECT_X,RECT_Y)

# in degree
def map_to_rectangle(x,y,angle):
    angle_rad=angle*(np.pi/180.0)
    vec=(np.cos(angle_rad),np.sin(angle_rad))
    # x=RECT_X
    min_dist=2*(RECT_X+RECT_Y)
    min_t=min_dist
    rec_coord=(0,0)
    if abs(vec[0])>=1e-2:
        t=(RECT_X-x)/vec[0]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            rec_coord=(RECT_X,y+t*vec[1])
        t=(-RECT_X-x)/vec[0]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            rec_coord=(-RECT_X,y+t*vec[1])
    if abs(vec[1])>=1e-2:
        t=(RECT_Y-y)/vec[1]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            rec_coord=(x+t*vec[0],RECT_Y)
        t=(-RECT_Y-y)/vec[1]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            rec_coord=(x+t*vec[0],-RECT_Y)
    return rec_coord, min_t

def path_planning(curx,cury,cur_angle,destx,desty,dest_angle):
    ev3.speaker.beep()
    start_rect,dist=map_to_rectangle(curx,cury,cur_angle)
    robot.straight(-dist)
    end_rect,dist=map_to_rectangle(destx,desty,dest_angle)
    # start X end >0 = counter clockwise
    cross=(start_rect[0]*end_rect[1]-start_rect[1]*end_rect[0])
    if cross>0:
        clockwise=False
    else:
        clockwise=True
    
    start_rect_vector=(start_rect[0]-curx,start_rect[1]-cury)
    ev3.speaker.beep()

def argmin(list):
    min_val=list[0]
    arg_min=0
    for i in range(len(list)):
        if list[i]<min_val:
            arg_min=i
            min_val=list[i]
    return arg_min

print(map_to_rectangle(100,100,45))