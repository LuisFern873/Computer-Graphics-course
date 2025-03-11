import os
import sys
import cv2
import numpy as np

def resize_image_bilinear(image, new_width, new_height):

    old_height, old_width = image.shape[:2]

    scale_x = float(old_width) / new_width
    scale_y = float(old_height) / new_height

    resized_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for y in range(new_height):
        for x in range(new_width):
            # Calculate the corresponding coordinates in the original image
            x_old = (x + 0.5) * scale_x - 0.5
            y_old = (y + 0.5) * scale_y - 0.5

            # Find the four nearest pixels in the original image
            x0 = int(x_old)
            y0 = int(y_old)
            x1 = min(x0 + 1, old_width - 1)
            y1 = min(y0 + 1, old_height - 1)

            # Perform bilinear interpolation
            dx = x_old - x0
            dy = y_old - y0
            top_left = image[y0, x0] * (1 - dx) * (1 - dy)
            top_right = image[y0, x1] * dx * (1 - dy)
            bottom_left = image[y1, x0] * (1 - dx) * dy
            bottom_right = image[y1, x1] * dx * dy

            # Assign the interpolated value to the output pixel
            resized_image[y, x] = top_left + top_right + bottom_left + bottom_right

    return resized_image

if __name__ == "__main__":

    image_path = sys.argv[1]
    new_height = int(sys.argv[2])
    new_width = int(sys.argv[3])

    input_image = cv2.imread(image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    resized_image = resize_image_bilinear(input_image, new_width, new_height)

    os.chdir('exercise01/output')
    cv2.imwrite(f"{image_path.removesuffix('.png')}_{new_height}_{new_width}.png", cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))


