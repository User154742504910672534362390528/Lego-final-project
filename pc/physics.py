import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lego"))

from const import *
import numpy as np
import os, sys

class Ball:
    def __init__(self, pos: np.array, index) -> None:
        self.index = index
        self.pos = pos
        self.radius = RADIUS
        self.potted = False

    def update(self, pos):
        self.pos = pos

    def path_clear(self, target: np.array, others: list) -> bool:
        # check if there are anything blocking the ball to the destination
        for ball in others:
            if ball is self:
                continue

        return False
    
def line_ball_collision(ball: Ball, p1: np.array, p2: np.array, distance: float) -> bool:
    # check if the distance from the ball to the line > distance
    if np.cross(p2 - p1, ball.pos - p1) / np.linalg.norm(p2 - p1) > distance:
        return False
    else:
        return True
    # if p1[0] == p2[0]:
    #     # vertical line
    #     if abs(p1[0] - ball.pos[0]) > distance:
    #         return False
    #     else:
    #         return True
    # else:
    #     line_slope = (p1[1] - p2[1])/(p1[0] - p2[0])
    #     normal = -1/line_slope
    #     np.cross()
    # return False

def ball_ball_collision(target_ball: Ball, balls:[]):
    for ball in balls:
        if not ball is not target_ball and abs(ball.pos - target_ball.pos) < target_ball.radius:
            return True

def plan_path(cue: Ball, billiard: Ball):

    pass