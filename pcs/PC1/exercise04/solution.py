import cv2
import os
import numpy as np

def projection_on_line(a, b, pixel):
    pa = pixel - a
    ba = b - a
    projection = a + np.dot(pa, ba) / np.dot(ba, ba) * ba
    return projection

def change_color_scale(image):

    rows, columns, dimensions = image.shape

    grid = np.ones((rows, columns, 3), dtype=np.uint8) * 255

    center = (columns // 2, rows // 2)
    radius = rows // 2
    color = (0, 0, 255)
    thickness = -1

    cv2.circle(grid, center, radius, color, thickness)

    black = np.array([0, 0, 0])
    # white = np.array([255, 255, 255])

    for i in range(rows):
        for j in range(columns):
            grid_pixel = np.array(grid[i, j])
            lenna_pixel = np.array(image[i, j])
            projection = projection_on_line(black, grid_pixel, lenna_pixel)
            image[i, j] = projection

if __name__ == "__main__":

    image_path = 'lenna.png'

    image = cv2.imread(image_path)

    change_color_scale(image)

    os.chdir('exercise04/output')
    cv2.imwrite(f"lenna-colorscale.png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    