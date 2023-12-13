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
robot.turn(360)