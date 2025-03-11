import cv2
import os
import sys
import numpy as np

def apply_kernel_RGB(image, kernel):
    rows, cols, channels = image.shape
    k_rows, k_cols = kernel.shape[:2]
    pad_rows = k_rows // 2
    pad_cols = k_cols // 2

    padded_image = cv2.copyMakeBorder(image, pad_rows, pad_rows, pad_cols, pad_cols, cv2.BORDER_CONSTANT, value=0) # Adding a border (proportional to the kernel order)

    result = np.zeros_like(image) # init filtered image

    for i in range(rows):
        for j in range(cols):
            for c in range(channels):
                roi = padded_image[i:i+k_rows, j:j+k_cols, c]
                result[i, j, c] = np.sum(roi * kernel)
            
    return result

def apply_kernel_grayscale(image, kernel):
    rows, cols = image.shape[:2]
    k_rows, k_cols = kernel.shape[:2]
    pad_rows = k_rows // 2
    pad_cols = k_cols // 2

    padded_image = cv2.copyMakeBorder(image, pad_rows, pad_rows, pad_cols, pad_cols, cv2.BORDER_CONSTANT, value=0) # Adding a border (proportional to the kernel order)

    result = np.zeros_like(image) # init filtered image

    for i in range(rows):
        for j in range(cols):
            roi = padded_image[i:i+k_rows, j:j+k_cols]
            result[i, j] = np.sum(roi * kernel)
    
    # m, M, _, _ = cv2.minMaxLoc(result)
    # print(m, M)

    return result

orders = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

def box_filter_grayscale(image):

    for order in orders:
        kernel = np.ones((order, order), dtype=np.float32) / pow(order, 2)
        filtered_image = apply_kernel_grayscale(image, kernel)
        
        cv2.imwrite(f"lenna-grayscale-box-filter-order-{order}.png", filtered_image)


def box_filter_rgb(image):
    for order in orders:
        kernel = np.ones((order, order, order), dtype=np.float32) / pow(order, 3)
        filtered_image = apply_kernel_RGB(image, kernel)
        
        cv2.imwrite(f"lenna-RGB-box-filter-order-{order}.png", filtered_image)

def bartlett_kernel(order):
    center = order // 2 + 1
    base = np.concatenate((np.arange(1, center), np.arange(center, 0, -1)))  
    kernel = np.outer(base, base)
    kernel = kernel / np.sum(kernel)
    return kernel

def bartlett_kernel_3d(order):
    center = order // 2 + 1
    base = np.concatenate((np.arange(1, center), np.arange(center, 0, -1)))  
    kernel = np.outer(base, base)
    kernel = np.tile(kernel, (order, 1, 1))
    kernel = kernel / np.sum(kernel)
    
    return kernel

def bartlett_filter_grayscale(image):

    for order in orders:
        kernel = bartlett_kernel(order)
        filtered_image = apply_kernel_grayscale(image, kernel)
        
        cv2.imwrite(f"lenna-grayscale-bartlett-filter-order-{order}.png", filtered_image)

def bartlett_filter_rgb(image):

    for order in orders:
        kernel = bartlett_kernel_3d(order)
        filtered_image = apply_kernel_RGB(image, kernel)
        cv2.imwrite(f"lenna-RGB-bartlett-filter-order-{order}.png", filtered_image)


def gaussian_kernel(order):
    base = np.zeros(order, dtype=int)
    base[0] = 1
    for i in range(1, order):
        base[i] = base[i - 1] * (order - i) // i
    kernel = np.outer(base, base)
    kernel = kernel / np.sum(kernel)
    return kernel


def gaussian_kernel_3d(order):
    base = np.zeros(order, dtype=int)
    base[0] = 1
    for i in range(1, order):
        base[i] = base[i - 1] * (order - i) // i
    kernel = np.outer(base, base)
    kernel = np.tile(kernel, (order, 1, 1))
    kernel = kernel / np.sum(kernel)
    return kernel

def gaussian_filter_grayscale(image):

    # A partir del order 17 el kernel contiene valores muy pequeños
    # y python castea esos valores a "-inf"

    for order in [3, 5, 7, 9, 11, 13, 15]:
        kernel = gaussian_kernel(order)
        filtered_image = apply_kernel_grayscale(image, kernel)
        cv2.imwrite(f"lenna-grayscale-gaussian-filter-order-{order}.png", filtered_image)

def gaussian_filter_rgb(image):

    # A partir del order 17 el kernel contiene valores muy pequeños
    # y python castea esos valores a "-inf"

    for order in [15]:
        kernel = gaussian_kernel_3d(order)
        filtered_image = apply_kernel_RGB(image, kernel)
        cv2.imwrite(f"lenna-RGB-gaussian-filter-order-{order}.png", filtered_image)


def laplacian_filter_grayscale(image):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    filtered_image = apply_kernel_grayscale(image, kernel)

    cv2.imwrite(f"lenna-grayscale-laplacian-filter-order-3.png", filtered_image)

    kernel = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [1, 2, -17, 2, 1],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 0, 0]
    ])
    filtered_image = apply_kernel_grayscale(image, kernel)

    cv2.imwrite(f"lenna-grayscale-laplacian-filter-order-5.png", filtered_image)


def laplacian_filter_rgb(image):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    # kernel = np.tile(kernel, (3, 1, 1))

    filtered_image = apply_kernel_RGB(image, kernel)

    cv2.imwrite(f"lenna-RGB-laplacian-filter-order-3.png", filtered_image)

    kernel = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [1, 2,-17,2, 1],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 0, 0]
    ])
    # kernel = np.tile(kernel, (5, 1, 1))
    filtered_image = apply_kernel_RGB(image, kernel)

    cv2.imwrite(f"lenna-RGB-laplacian-filter-order-5.png", filtered_image)


if __name__ == "__main__":
    
    # image_grayscale = cv2.imread("lenna.png", cv2.IMREAD_GRAYSCALE)
    image_rgb = cv2.imread("lenna.png")
    
    # os.chdir('exercise05/output')
    laplacian_filter_rgb(image_rgb)
    

    # # box_filter_grayscale(image_grayscale)
    # # box_filter_rgb(image_rgb)
    # cv2.imshow('image', image_grayscale)
    
    

    # cv2.imshow('filtered image', filtered_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()