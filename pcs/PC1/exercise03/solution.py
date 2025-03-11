import cv2

def change_brighness(image, constant):

    height, width = image.shape[:2]

    for i in range(height):
        for j in range(width):
                if image[i, j] + constant > 255:
                    image[i, j] = 255
                elif image[i, j] + constant < 0:
                    image[i, j] = 0
                else:
                    image[i, j] = image[i, j] + constant

def change_contrast(image, m, M, new_m, new_M):
     
    height, width = image.shape[:2]
    
    for i in range(height):
        for j in range(width):
            image[i, j] = new_m + ((image[i, j] - m) / (M - m)) * (new_M - new_m)

def nothing(pos):
    pass

if __name__ == '__main__':

    image_path = 'lenna.png'

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    cv2.namedWindow('image')
    cv2.createTrackbar('Contrast', 'image', 5, 10, nothing)

    m, M, _, _ = cv2.minMaxLoc(image) # color range [m, M]
    m_scaling = m // 5
    M_scaling = (255 - M) // 5

    mapping = {
        0 : (m + (5 * m_scaling), M - (5 * M_scaling)), # Bajo contraste
        1 : (m + (4 * m_scaling), M - (4 * M_scaling)),
        2 : (m + (3 * m_scaling), M - (3 * M_scaling)),
        3 : (m + (2 * m_scaling), M - (2 * M_scaling)),
        4 : (m + (1 * m_scaling), M - (1 * M_scaling)),
        5 : (m, M),
        6 : (m - (1 * m_scaling), M + (1 * M_scaling)),
        7 : (m - (2 * m_scaling), M + (2 * M_scaling)),
        8 : (m - (3 * m_scaling), M + (3 * M_scaling)),
        9 : (m - (4 * m_scaling), M + (4 * M_scaling)), # Alto contraste
        10 : (0, 255)
    }

    while True: 
        cv2.imshow('image', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # Presione 'q' para salir
            break
        
        pos = cv2.getTrackbarPos('Contrast', 'image') 
        new_m, new_M = mapping[pos]
        
        change_contrast(image, m, M, new_m, new_M)

        m = new_m
        M = new_M

    cv2.destroyAllWindows()