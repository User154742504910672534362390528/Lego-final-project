# from pathlib import Path
# import sys
# __package__ = Path(__file__).parent.resolve()
# print(__package__)
# print(__spec__)
# from __future__ import absolute_import
# from lego

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