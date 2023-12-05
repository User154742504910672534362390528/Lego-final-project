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

    def __str__(self) -> str:
        s = f"{self.index}: pos={self.pos}, potted={self.potted}"
        return s

    def update(self, pos):
        '''
        update the position of the ball
        '''
        self.pos = pos

    def path_clear(self, target: np.array, others: list) -> bool:
        '''
        check if there are anything blocking the ball to the destination
        '''
        for ball in others:
            if ball is self:
                continue
            if line_ball_collision(ball, self.pos, target, ball.radius + self.radius):
                return False

        return True
    
    
def line_ball_collision(ball: Ball, p1: np.array, p2: np.array, distance: float) -> bool:
    '''
    check if the distance from the ball to the line > distance
    '''
    if abs(np.cross(p2 - p1, ball.pos - p1) / np.linalg.norm(p2 - p1)) > distance:
        return False
    else:
        return True

def ball_ball_collision(target_ball: Ball, balls:list[Ball]) -> bool:
    for ball in balls:
        if not ball is not target_ball and abs(ball.pos - target_ball.pos) < target_ball.radius:
            return True

def plan_path(cue: Ball, billiard: list[Ball]):
    '''
    Brute force all possible combinations of balls an pockets to find a feasible path
    You can you up!
    '''

    for ball in billiard:
        for p1, p2 in CORNER_POCKET_POS:
            pass
        for p1, p2 in MID_POCKET_POS:
            pass