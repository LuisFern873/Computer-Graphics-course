import cv2
import numpy as np


# In Computer graphics class

def change_contrast(img, new_m, new_M):

    # img in [m, M]

    m = np.min(img)
    M = np.max(img)

    img = new_m + ((img - m) / (M - m)) * (new_M - new_m)

    img = np.clip(img, new_m, new_M)

    return img.astype(np.uint8)


# In Computer Vision class
# brightness:   I'(x, y) = I(x, y) + B
# contrast:     I'(x, y) = (I(x, y) + u)C + u
# u es la media de intensidades

def function(img, brightness=0, contrast=1.0):

    img = img.astype(np.float32)

    u = np.mean(img)

    img = (img - u) * contrast + u + brightness
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)



def on_trackbar(val):
    brightness = cv2.getTrackbarPos("Brillo", "Ajustes") - 100
    contrast = cv2.getTrackbarPos("Contraste", "Ajustes") / 50.0
    adjusted = function(img, brightness, contrast)
    cv2.imshow("Ajustes", adjusted)


img = cv2.imread("lenna.png")

cv2.namedWindow("Ajustes")
cv2.createTrackbar("Brillo", "Ajustes", 100, 200, on_trackbar)
cv2.createTrackbar("Contraste", "Ajustes", 50, 100, on_trackbar)

on_trackbar(0)
cv2.waitKey(0)
cv2.destroyAllWindows()