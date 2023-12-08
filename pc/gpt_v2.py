import math

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def is_near_pocket(ball, holes, RADIUS):
    for hole in holes:
        dist_to_hole = distance(ball, hole)
        if dist_to_hole < RADIUS:
            return True
    return False

def has_clear_path(ball, other_balls, RADIUS):
    return all(distance(ball, other_ball) > RADIUS for other_ball in other_balls)

def choose_shot(cue, balls, holes, RADIUS):
    best_shot_index = None
    best_score = float('-inf')

    for i, target_ball in enumerate(balls):
        if distance(cue, target_ball) > 2 * RADIUS:
            # Calculate the score based on proximity to pockets and clear path
            score = 0
            if is_near_pocket(target_ball, holes, RADIUS):
                # The target ball is close to a pocket
                score += 1
            else:
                # Check if there is a clear path to the pocket
                clear_path = has_clear_path(target_ball, [ball for j, ball in enumerate(balls) if j != i], RADIUS)
                if clear_path:
                    score += 0.5

            # Update the best shot if the current one has a higher score
            if score > best_score:
                best_score = score
                best_shot_index = i

    return best_shot_index

# Example usage:
cue_position = (9, 0)
ball_positions = [(1, 1), (2, 2), (3, 3)]  # Replace with actual ball positions
hole_positions = [(10, 10), (-10, -10)]  # Replace with actual hole positions
RADIUS = 1  # Replace with actual ball radius

best_shot = choose_shot(cue_position, ball_positions, hole_positions, RADIUS)
print("Best shot index:", best_shot)
