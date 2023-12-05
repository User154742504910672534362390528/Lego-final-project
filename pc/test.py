from physics import *

b = Ball(np.array([100, 200]), 0)
balls = []
for i in range(5):
    balls.append(Ball(np.array([i*100, i*200]), i))
balls.append(b)
print(b)
p1 = np.array([0, 230])
p2 = np.array([200, 230])
print(line_ball_collision(b, p1, p2, 2*RADIUS))
b.path_clear(np.array([1,2]), balls)