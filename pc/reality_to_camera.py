import numpy as np
scale = 0.9
CAMERA_MTX = np.array(
    [
        [650.59819165*scale, 0.        ,320.0],
        [  0.        ,653.61004762*scale ,240.0],
        [  0.          ,0.          ,1.        ]
    ]
)
x=0
y=0

vec_cam=(x/310,-y/310,1)
print(CAMERA_MTX@vec_cam)