import numpy as np
host_ip = "169.254.98.60"
client_ip = "169.254.62.193"
PORT = 8964
QUIT_MSG = "bye"
HELP_MSG = "help"

HELP_PROMPT = \
'''
Beep: beep
Turn motor: turn [port (A)] [speed] [angle]
Go: go [speed] [turn_rate]
'''

# ball related
RADIUS = 15 # mm

# TODO
# center, 2 corners
'''
    |
   2|
   /  ___________     ______
  (_/ 1          \   /
  0               |_|
'''
CORNER_POCKET_POS = [
    [np.array([0, 0]), np.array([28.929, 0]), np.array([7.6772, 29.1666])],
    [np.array([0, 268.07]), np.array([28.929, 268.07]), np.array([7.6772, 268.07-29.1666])],
    [np.array([557.4, 0]), np.array([557.4-28.929, 0]), np.array([557.04-7.6772, 0+29.1666])],
    [np.array([557.4, 268.07]), np.array([557.4-28.929, 268.07]), np.array([557.4-7.6772, 268.07-29.1666])],
]

# corner - radius
CORNER_AIM_POS = np.array(
    [
        np.array([7.6772+RADIUS, 0+RADIUS]),
        np.array([7.6772+RADIUS, 268.07-RADIUS]),
        np.array([557.4-RADIUS, 0+RADIUS]),
        np.array([557.4-RADIUS, 268.07-RADIUS])
    ]
)

# center, 2 outer corners, 2 inner corners
'''
____     ____
   1\   /2
 3__/|_|\___4
      0

radius = 39
'''
MID_POCKET_POS = [
    [
        np.array([278.7, -21.85]), 
        np.array([278.7-32.19, 0]), 
        np.array([278.7+32.19, 0]), 
        np.array([278.7-17.6111, -16.85]), 
        np.array([278.7+17.6111, -16.85]),
    ],
    [
        np.array([278.7, 268.07+21.85]), 
        np.array([278.7-32.19, 268.07]), 
        np.array([278.7+32.19, 268.07]), 
        np.array([278.7-17.6111, 268.07+16.85]), 
        np.array([278.7+17.6111, 268.07+16.85]),
    ]
]

MID_AIM_POS = np.array(
    [
        
    ]
)

# TODO
CORNER_POCKET_ANGLES = [
    45, 45
]

MID_POCKET_ANGLE = [
    -45, 45
]
# corner center to mid center: 278.7 mm, 21.85
# mid open: 64.38, 35.2221
#           32.19, 17.6111
# corner to corner 27