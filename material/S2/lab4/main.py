import cv2
import numpy as np

# Exercises 1, 2, 3

lenna = cv2.imread('lenna.png')
grid = cv2.imread('colors.png')

rows, columns, dimensions = lenna.shape

# black and white represent the achromatic line in 3D space.
black = np.array([0, 0, 0])
white = np.array([255, 255, 255])

# lines defined by specific colors
red = np.array([0, 0, 255]) # R
green = np.array([0, 255, 0]) # G
blue = np.array([255, 0, 0]) # B

# The line is defined by the points a and b
def projection_on_line(a, b, pixel):
    pa = pixel - a
    ba = b - a
    projection = a + np.dot(pa, ba) / np.dot(ba, ba) * ba
    return projection

def exercise_1():
    for i in range(rows):
        for j in range(columns):
            pixel = np.array(lenna[i, j])
            projection = projection_on_line(black, white, pixel)
            lenna[i, j] = projection

def exercise_2(color):
    for i in range(rows):
        for j in range(columns):
            pixel = np.array(lenna[i, j])
            projection = projection_on_line(black, color, pixel)
            lenna[i, j] = projection

def exercise_3():
    for i in range(rows):
        for j in range(columns):
            grid_pixel = np.array(grid[i, j])
            lenna_pixel = np.array(lenna[i, j])
            projection = projection_on_line(black, grid_pixel, lenna_pixel)
            lenna[i, j] = projection


exercise_3()

cv2.imshow('imagen', lenna)
cv2.waitKey(0)
cv2.destroyAllWindows()

