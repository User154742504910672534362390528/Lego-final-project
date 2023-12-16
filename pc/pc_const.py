import numpy as np
import cv2


# This part is for logitech c920
AREA_THRESH_MAX = 500
AREA_THRESH_MIN = 60
CIRCLE_RADIUS = 10
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (CIRCLE_RADIUS, CIRCLE_RADIUS))
kernel = kernel | kernel.T
HMin, HMax = 86, 118
SMin, SMax = 0, 92
VMin, VMax = 69, 158