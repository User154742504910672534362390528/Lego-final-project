#!/usr/bin/env pybricks-micropython
from robot_inc import *
import time

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()
# Initialize the motors.
motor_0 = Motor(Port.D)
motor_1 = Motor(Port.A,positive_direction=Direction.COUNTERCLOCKWISE)
motor_0.reset_angle(450)
motor_1.reset_angle(0)
arm = DriveBase(motor_0,motor_1,wheel_diameter=1,axle_track=1)
cur_angle=(450,0)

z = 40 #input
theta = 60 * pi/180 #input

h = 27.75
d1 = 195
d2 = 44.1814
d3 = 264
d4 = 32
d5 = 132 #改
d6 = 24
v0_x = 62.494
v0_y = 137.399
v1_x = 128.041
v1_y = 129.944

theta_1 = asin((z - d6 * cos(theta) + d5 * sin(theta) - h - v1_y)/d1)
theta_2_a = atan2((d1 * sin(theta_1) + d4 * sin(theta) - v0_y + v1_y), (d1 * cos(theta_1) - d4 * cos(theta) - v0_x + v1_x))
l = sqrt((d1 * sin(theta_1) + d4 * sin(theta) - v0_y + v1_y)**2 + (d1 * cos(theta_1) - d4 * cos(theta) - v0_x + v1_x)**2)
theta_2_b = acos((d2**2 + l**2 - d3**2) / (2 * d2 * l))
theta_2 = theta_2_a + theta_2_b
d = d6 * sin(theta) + (d4 + d5) * cos(theta) + l * cos(theta_2_a) + v0_x
print("d = ", d)

angle_1 = theta_1 * 180 / pi
angle_2 = theta_2 * 180 / pi
print("Target angle of Motor 0:", angle_2)
print("Target angle of Motor 1:", angle_1)

motor_0.run_target(100, angle_2 * 5)
motor_1.run_target(100, angle_1 * 5)

m0=angle_2 * 5
m1=angle_1 * 5
time.sleep(6)
motor_1.run_target(100, 0)
motor_0.run_target(100, 450)

current_angle_0 = motor_0.angle()
current_angle_1 = motor_1.angle()
print("Current angle of Motor 0:", current_angle_0)
print("Current angle of Motor 1:", current_angle_1)