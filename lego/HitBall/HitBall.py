#!/usr/bin/env pybricks-micropython
from robot_inc import *
from parameters import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()
# Initialize the motors.
left_motor = Motor(Port.B,positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.C,positive_direction=Direction.COUNTERCLOCKWISE)
motor_0 = Motor(Port.D)
motor_1 = Motor(Port.A,positive_direction=Direction.COUNTERCLOCKWISE)
motor_0.reset_angle(450)
motor_1.reset_angle(0)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
arm = DriveBase(motor_0,motor_1,wheel_diameter=1,axle_track=1)

# Current Position
cur_pos=(RECT_X,RECT_Y,180)

def HitBall(x,y,longtitude,latitude):
    t1,t2,d=decide_t1_t2(Z,latitude)
    end_point=(x+8*sin(longtitude)-d*cos(longtitude),y-8*cos(longtitude)-d*sin(longtitude),longtitude)
    t1_h,t2_h,_=decide_t1_t2(Z+26,latitude-6)
    move_t1_t2(t1_h,t2_h)
    path_planning(cur_pos[0],cur_pos[1],cur_pos[2],end_point[0],end_point[1],end_point[2])
    cur_pos=end_point
    move_t1_t2(t1,t2)

def decide_t1_t2(z,theta_deg):
    theta=theta_deg*pi/180
    theta_1 = asin((z - d6 * cos(theta) + d5 * sin(theta) - h - v1_y)/d1)
    theta_2_a = atan2((d1 * sin(theta_1) + d4 * sin(theta) - v0_y + v1_y), (d1 * cos(theta_1) - d4 * cos(theta) - v0_x + v1_x))
    l_square = (d1 * sin(theta_1) + d4 * sin(theta) - v0_y + v1_y)**2 + (d1 * cos(theta_1) - d4 * cos(theta) - v0_x + v1_x)**2
    theta_2_b = acos((d2**2 + l_square - d3**2) / (2 * d2 * sqrt(l_square)))
    d=d6 * sin(theta) + (d4 + d5) * cos(theta) + sqrt(l_square) * cos(theta_2_a) + v0_x
    theta_1_deg=theta_1*180/pi
    theta_2_deg=(theta_2_a+theta_2_b)*180/pi
    return theta_1_deg,theta_2_deg,d

def move_t1_t2(t1,t2):
    motor_0.run_target(100, t2 * 5)
    motor_1.run_target(100, t1 * 5)

def path_planning(curx,cury,cur_angle,destx,desty,dest_angle):
    ev3.speaker.beep()
    start_rect,start_dist,start_edge=map_to_rectangle(curx,cury,cur_angle)
    robot.straight(start_dist)
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
                robot.straight(RECT_X-cur_pos[0])
                cur_pos=(RECT_X,-RECT_Y)
            elif cur_edge==1:
                robot.straight(RECT_Y-cur_pos[1])
                cur_pos=(RECT_X,RECT_Y)
            elif cur_edge==2:
                robot.straight(RECT_X+cur_pos[0])
                cur_pos=(-RECT_X,RECT_Y)
            elif cur_edge==3:
                robot.straight(RECT_Y+cur_pos[1])
                cur_pos=(-RECT_X,-RECT_Y)
            cur_edge=(cur_edge+1)%4
            robot.turn(90)
        if end_edge==0:
            robot.straight(end_rect[0]-cur_pos[0])
        elif end_edge==1:
            robot.straight(end_rect[1]-cur_pos[1])
        elif end_edge==2:
            robot.straight(cur_pos[0]-end_rect[0])
        elif end_edge==3:
            robot.straight(cur_pos[1]-end_rect[1])
        robot.turn(reg_angle(90*end_edge,dest_angle))
    else:
        robot.turn(reg_angle(cur_angle,90*(start_edge+2)))
        while cur_edge != end_edge:
            if cur_edge==0:
                robot.straight(RECT_X+cur_pos[0])
                cur_pos=(-RECT_X,-RECT_Y)
            elif cur_edge==1:
                robot.straight(RECT_Y+cur_pos[1])
                cur_pos=(RECT_X,-RECT_Y)
            elif cur_edge==2:
                robot.straight(RECT_X-cur_pos[0])
                cur_pos=(RECT_X,RECT_Y)
            elif cur_edge==3:
                robot.straight(RECT_Y-cur_pos[1])
                cur_pos=(-RECT_X,RECT_Y)
            cur_edge=(cur_edge+3)%4
            robot.turn(-90)
        if end_edge==0:
            robot.straight(cur_pos[0]-end_rect[0])
        elif end_edge==1:
            robot.straight(cur_pos[1]-end_rect[1])
        elif end_edge==2:
            robot.straight(end_rect[0]-cur_pos[0])
        elif end_edge==3:
            robot.straight(end_rect[1]-cur_pos[1])
        robot.turn(reg_angle(90*(end_edge+2),dest_angle))
    robot.straight(-end_dist)
    ev3.speaker.beep()

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
