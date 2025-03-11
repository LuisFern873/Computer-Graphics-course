import os
import sys
import cv2
import numpy as np

def create_colored_board(H_PIXELS, W_PIXELS, H_CELLS, W_CELLS):

    colors = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]  # (B, G, R) format

    board = np.zeros((H_PIXELS, W_PIXELS, 3), dtype=np.uint8)
    cell_height = H_PIXELS // H_CELLS
    cell_width = W_PIXELS // W_CELLS

    for i in range(H_CELLS):
        for j in range(W_CELLS):
            color_index = (i + j) % len(colors)
            color = colors[color_index]
            cell_top_left = (j * cell_width, i * cell_height)
            cell_bottom_right = ((j + 1) * cell_width, (i + 1) * cell_height)
            cv2.rectangle(board, cell_top_left, cell_bottom_right, color, -1)

    return board

if __name__ == "__main__":

    h_pixels = int(sys.argv[1])
    w_pixels = int(sys.argv[2])
    h_cells = int(sys.argv[3])
    w_cells = int(sys.argv[4])

    # H PIXELS, W PIXELS, H CELLS, W CELLS
    # produces an image of H PIXELS x W PIXELS pixels, which consists of a board of H CELLS of height and W CELLS of width.

    board = create_colored_board(h_pixels, w_pixels, h_cells, w_cells)

    os.chdir('exercise02/output')
    cv2.imwrite(f"board_{h_pixels}_{h_cells}_{w_pixels}_{w_cells}.png", cv2.cvtColor(board, cv2.COLOR_RGB2BGR))