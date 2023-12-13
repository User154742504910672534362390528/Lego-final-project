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
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=180)

# Go forward and backwards for one meter.
# forward(400)
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
    angle_rad=angle*(pi/180.0)
    vec=(cos(angle_rad),sin(angle_rad))
    # x=RECT_X
    min_dist=2*(RECT_X+RECT_Y)
    min_t=min_dist
    rec_coord=(0,0)
    edge=0
    if abs(vec[0])>=1e-2:
        t=(RECT_X-x)/vec[0]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            edge=1
            rec_coord=(RECT_X,y+t*vec[1])
        t=(-RECT_X-x)/vec[0]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            edge=3
            rec_coord=(-RECT_X,y+t*vec[1])
    if abs(vec[1])>=1e-2:
        t=(RECT_Y-y)/vec[1]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            edge=2
            rec_coord=(x+t*vec[0],RECT_Y)
        t=(-RECT_Y-y)/vec[1]
        if abs(t)<min_dist:
            min_dist=abs(t)
            min_t=t
            edge=0
            rec_coord=(x+t*vec[0],-RECT_Y)
    return rec_coord, min_t, edge

def reg_angle(start,end):
    rotate=(end-start+3600)%360
    rotate_opposite=-((360-rotate)%360)
    if abs(rotate)<abs(rotate_opposite):
        return rotate
    else:
        return rotate_opposite

def path_planning(curx,cury,cur_angle,destx,desty,dest_angle):
    ev3.speaker.beep()
    start_rect,start_dist,start_edge=map_to_rectangle(curx,cury,cur_angle)
    forward(-start_dist)
    end_rect,end_dist,end_edge=map_to_rectangle(destx,desty,dest_angle)
    # start X end >0 = counter clockwise
    cross=(start_rect[0]*end_rect[1]-start_rect[1]*end_rect[0])
    if cross>0:
        counter_clockwise=True
    else:
        counter_clockwise=False
    cur_edge=start_edge
    cur_pos=list(start_rect)
    if counter_clockwise==True:
        robot.turn(reg_angle(cur_angle,90*start_edge))
        while cur_edge != end_edge:
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
        if end_edge==0:
            forward(end_rect[0]-cur_pos[0])
        elif end_edge==1:
            forward(end_rect[1]-cur_pos[1])
        elif end_edge==2:
            forward(end_rect[0]+cur_pos[0])
        elif end_edge==3:
            forward(end_rect[1]+cur_pos[1])
        robot.turn(reg_angle(90*end_edge,dest_angle))
    else:
        robot.turn(reg_angle(cur_angle,90*(dest_angle+2)))
        while cur_edge != end_edge:
            if cur_edge==0:
                forward(RECT_X+cur_pos[0])
                cur_pos=(-RECT_X,-RECT_Y)
            elif cur_edge==1:
                forward(RECT_Y+cur_pos[1])
                cur_pos=(RECT_X,-RECT_Y)
            elif cur_edge==2:
                forward(RECT_X-cur_pos[0])
                cur_pos=(RECT_X,RECT_Y)
            elif cur_edge==3:
                forward(RECT_Y-cur_pos[1])
                cur_pos=(-RECT_X,RECT_Y)
            cur_edge=(cur_edge+3)%4
            robot.turn(-90)
        if end_edge==0:
            forward(end_rect[0]-cur_pos[0])
        elif end_edge==1:
            forward(end_rect[1]-cur_pos[1])
        elif end_edge==2:
            forward(end_rect[0]+cur_pos[0])
        elif end_edge==3:
            forward(end_rect[1]+cur_pos[1])
        robot.turn(reg_angle(90*end_edge,dest_angle))

    ev3.speaker.beep()

def argmin(list):
    min_val=list[0]
    arg_min=0
    for i in range(len(list)):
        if list[i]<min_val:
            arg_min=i
            min_val=list[i]
    return arg_min

def forward(dist):
    forward(-dist)
print(map_to_rectangle(400,100,45))