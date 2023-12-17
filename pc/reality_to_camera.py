import numpy as np
CAMERA_MTX = np.array(
    [
        [650.59819165, 0.        ,317.94835167],
        [  0.        ,653.61004762 ,242.65273137],
        [  0.          ,0.          ,1.        ]
    ]
)
x=135
y=65

vec_cam=(x/300,-y/300,1)
print(CAMERA_MTX@vec_cam)