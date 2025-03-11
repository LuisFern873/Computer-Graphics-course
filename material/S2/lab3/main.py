import cv2

img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)

rows, columns, dimensions = img.shape

brightness = 100
slider = 0



class lab:
    def __init__(self):
        pass

    @staticmethod
    def brightness(relative):
        # Brightness
        for i in range(rows):
            for j in range(columns):
                img[i, j, 0] = brightness + img[i, j, 0]
                img[i, j, 1] = brightness + img[i, j, 1]
                img[i, j, 2] = brightness + img[i, j, 2]
    
    @staticmethod
    def contrast(relative):
        # Contrast 
        for i in range(rows):
            for j in range(columns):
                pass
        
        pass


lab.brightness(brightness)



cv2.imshow('imagen', img)
cv2.waitKey(0)
cv2.destroyAllWindows()