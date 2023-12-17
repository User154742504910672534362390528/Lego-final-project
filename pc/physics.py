import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lego"))

from const import *
import numpy as np
import os, sys
from numpy.linalg import solve

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

    # TODO
    def path_clear(self, target: np.array, others: list) -> int:
        '''
        check if there are anything blocking the ball to the destination
        return the number of balls blocking to the hole, 0 for clear
        '''
        blocks = 0
        for ball in others:
            if ball is self:
                continue
            if ball.line_ball_collision(self.pos, target, ball.radius + self.radius):
                blocks += 1

        return blocks
    
    def line_ball_collision(self, p1: np.array, p2: np.array, distance: float) -> bool:
        '''
        check if the distance from the ball to the line > distance
        '''
        if abs(np.cross(p2 - p1, self.pos - p1) / np.linalg.norm(p2 - p1)) > distance:
            return False
        else:
            return True
        
    def find_opposite_position(self, hole: np.array, hole_index: int)-> np.array:
        '''
        find the intersection between the line from hole to ball and the table
        hole_index: corner between const.TABLE[hole_index:hole_index+2]
        '''
        x = [self.pos[0], hole[0]]
        y = [self.pos[1], hole[1]]
        coefficient = np.polyfit(x, y, 1)
        table_line_index = (hole_index + 2)%4
        table_line = TABLE[table_line_index]
        print("cof", coefficient)
        print("var", [[table_line[0], coefficient[0]], [table_line[1], -1]])
        # y = c[0] * x + c[1]
        # c0 * x + -1 * y = -c1 # hole-ball line
        cof = np.array([[table_line[0], coefficient[0]], [table_line[1], -1]])
        consts = np.array([table_line[2], coefficient[1]])
        solution = solve(cof, consts)
        solx, soly = solution
        print("sol", solution)
        if solx > 135 or solx < -135 or soly > 65 or soly < -65:
            print("wrong line")
            table_line_index += 1
            table_line_index %=4
            table_line = TABLE[table_line_index]
            print("cof", coefficient)
            print("var", [[table_line[0], coefficient[0]], [table_line[1], -1]])
            # y = c[0] * x + c[1]
            # c0 * x + -1 * y = -c1 # hole-ball line
            cof = np.array([[table_line[0], coefficient[0]], [table_line[1], -1]])
            consts = np.array([table_line[2], coefficient[1]])
            solution = solve(cof, consts)
            solx, soly = solution
            print("sol", solution)

        return solution

def ball_ball_collision(target_ball: Ball, balls:list[Ball]) -> bool:
    for ball in balls:
        if not ball is not target_ball and abs(ball.pos - target_ball.pos) < target_ball.radius:
            return True

def in_pillars(pos: np.array)->bool:
    '''
    check if the position is in between the pillars of the pool table.
    true if in pillar
    '''
    x = pos[0]
    y = pos[1]
    if x > -35 and x < 35:
        return True
    return False

def distance(p1:np.array, p2:np.array)->float:
    # print(p1, p2)
    return np.linalg.norm(p1-p2)

# TODO
def plan_path(balls: list[Ball], holes: list[list[int]]):
    '''
    Brute force all possible combinations of balls and pockets to find a feasible path
    You can you up!
    '''
    best_shot = []
    best_score = -1
    for ball in balls:
        for i, hole in enumerate(holes):
            score = ball.path_clear(hole, balls)
            # if score == 0:
            #     # possible shot
            #     best_shot.append([ball, hole])
            print(hole)
            opposite_pos = ball.find_opposite_position(hole, i)
            # scale heuristic by some constant
            score *= 10
            score += in_pillars(opposite_pos)
            score += distance(opposite_pos, ball.pos)

            if score <= best_score:
                best_shot = [ball, hole]
                best_score = score

    return best_shot