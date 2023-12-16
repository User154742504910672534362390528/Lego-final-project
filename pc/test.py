from physics import *

b = Ball(np.array([100, 200]), 0)
balls = []
for i in range(1, 7):
    if i == 1: continue
    balls.append(Ball(np.array([i*100, i*200]), i))
balls.append(b)
print(b)
for ball in balls:
    print(ball)
p1 = np.array([0, 230])
p2 = np.array([200, 230])
# print(line_ball_collision(b, p1, p2, 2*RADIUS))
print(b.path_clear(np.array([600, 300]), balls))

print(plan_path(balls, [[100, 100]]))