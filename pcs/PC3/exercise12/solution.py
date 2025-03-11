import numpy as np
from PIL import Image
import os

def load_mesh(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    vertices = []
    faces = []
    
    for line in lines:
        parts = line.split()
        if parts[0] == 'v':
            vertices.append(list(map(float, parts[1:])))
        elif parts[0] == 'f':
            faces.append(list(map(int, parts[1:])))
    
    vertices = np.array(vertices)
    faces = np.array(faces) - 1  # Convert to zero-indexed
    return vertices, faces

def project_vertex(vertex):
    return vertex[:2] / vertex[2]

def project_triangle(triangle):
    return np.array([project_vertex(v) for v in triangle])

def calculate_normal(triangle):
    v1, v2, v3 = triangle
    normal = np.cross(v2 - v1, v3 - v1)
    normal /= np.linalg.norm(normal)
    return normal

def cosine_illumination(normal):
    view_vector = np.array([0, 0, 1])
    return max(0, np.dot(normal, view_vector))

def draw_triangle(image, projected_triangle, intensity, min_x, max_x, min_y, max_y, width, height):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    
    def to_image_coords(x, y):
        ix = int((x - min_x) / (max_x - min_x) * width)
        iy = int((y - min_y) / (max_y - min_y) * height)
        return ix, height - iy  # Flip y-axis for image coordinates
    
    pts = [to_image_coords(x, y) for x, y in projected_triangle]
    color = int(255 * intensity)
    draw.polygon(pts, fill=(color, color, color))

def painter_algorithm_simple_cosine_illuminatio(
        full_path_input_mesh,
        full_path_output_image,
        min_x_coordinate_in_projection_plane,
        min_y_coordinate_in_projection_plane,
        max_x_coordinate_in_projection_plane,
        max_y_coordinate_in_projection_plane,
        width_in_pixels,
        height_in_pixels):
    
    vertices, faces = load_mesh(full_path_input_mesh)
    
    triangles = [vertices[face] for face in faces]
    projected_triangles = [project_triangle(triangle) for triangle in triangles]
    
    distances = [max(np.linalg.norm(vertex) for vertex in triangle) for triangle in triangles]
    sorted_indices = np.argsort(distances)[::-1]  # Sort in descending order
    
    image = Image.new('RGB', (width_in_pixels, height_in_pixels), (0, 0, 0))
    
    for i in sorted_indices:
        triangle = triangles[i]
        projected_triangle = projected_triangles[i]
        normal = calculate_normal(triangle)
        intensity = cosine_illumination(normal)
        draw_triangle(image, projected_triangle, intensity, min_x_coordinate_in_projection_plane, 
                      max_x_coordinate_in_projection_plane, min_y_coordinate_in_projection_plane, 
                      max_y_coordinate_in_projection_plane, width_in_pixels, height_in_pixels)
    
    image.save(full_path_output_image)

# Example usage
painter_algorithm_simple_cosine_illuminatio(
    full_path_input_mesh='sphere-rectangles.off',
    full_path_output_image='photo-of-sphere.png',
    min_x_coordinate_in_projection_plane=-1.0,
    min_y_coordinate_in_projection_plane=-1.0,
    max_x_coordinate_in_projection_plane=1.0,
    max_y_coordinate_in_projection_plane=1.0,
    width_in_pixels=640,
    height_in_pixels=480
)
