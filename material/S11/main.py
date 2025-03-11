import pygame
import numpy as np

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Triangle Projection")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# simple triangle in 3D space (x, y, z)
triangle_vertices = np.array([
    [0, 1, 5],
    [-1, -1, 5],
    [1, -1, 5]
])



# Camera parameters
fov = 90  # Field of view
aspect_ratio = width / height
near_plane = 0.1
far_plane = 1000.0


# Camera







# Projection matrix
fov_rad = 1 / np.tan(np.radians(fov) / 2)
projection_matrix = np.array([
    [aspect_ratio * fov_rad, 0, 0, 0],
    [0, fov_rad, 0, 0],
    [0, 0, far_plane / (far_plane - near_plane), 1],
    [0, 0, (-far_plane * near_plane) / (far_plane - near_plane), 0]
])

def project(vertex, matrix):
    # Apply the projection matrix
    projected_vertex = np.dot(matrix, vertex)
    # Normalize
    if projected_vertex[3] != 0:
        projected_vertex /= projected_vertex[3]
    return projected_vertex




def draw_triangle(vertices, color):
    projected_vertices = [project(vertex, projection_matrix) for vertex in vertices]
    screen_coords = [
        ((vertex[0] + 1) * 0.5 * width, (1 - (vertex[1] + 1) * 0.5) * height)
        for vertex in projected_vertices
    ]
    pygame.draw.polygon(screen, color, screen_coords, 1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Convert 3D vertices to 4D homogeneous coordinates
    homogeneous_vertices = [np.append(vertex, 1) for vertex in triangle_vertices]

    # Draw the triangle
    draw_triangle(homogeneous_vertices, WHITE)

    pygame.display.flip()

pygame.quit()
