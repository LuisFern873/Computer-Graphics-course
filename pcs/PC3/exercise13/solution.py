import numpy as np
from PIL import Image
import os

def load_mesh(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    vertices = []
    texture_coords = []
    faces = []
    
    for line in lines:
        parts = line.split()
        if parts[0] == 'v':
            vertices.append(list(map(float, parts[1:])))
        elif parts[0] == 'vt':
            texture_coords.append(list(map(float, parts[1:])))
        elif parts[0] == 'f':
            face = [list(map(int, part.split('/'))) for part in parts[1:]]
            faces.append(face)
    
    vertices = np.array(vertices)
    texture_coords = np.array(texture_coords)
    return vertices, texture_coords, faces

def project_vertex(vertex):
    return vertex[:2] / vertex[2]

def project_triangle(triangle):
    return np.array([project_vertex(v) for v in triangle])

def barycentric_coords(p, a, b, c):
    v0 = b - a
    v1 = c - a
    v2 = p - a
    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    return u, v, w

def draw_triangle(image, projected_triangle, texture_triangle, texture_image, min_x, max_x, min_y, max_y, width, height):
    from PIL import ImageDraw, ImageOps
    draw = ImageDraw.Draw(image)
    
    def to_image_coords(x, y):
        ix = int((x - min_x) / (max_x - min_x) * width)
        iy = int((y - min_y) / (max_y - min_y) * height)
        return ix, height - iy  # Flip y-axis for image coordinates
    
    def get_texture_color(u, v):
        texture_width, texture_height = texture_image.size
        tex_x = int(u * texture_width)
        tex_y = int((1 - v) * texture_height)  # Flip v coordinate
        return texture_image.getpixel((tex_x, tex_y))
    
    pts = [to_image_coords(x, y) for x, y in projected_triangle]
    bbox = ImageOps.boundingbox(image)
    bbox = [max(bbox[0], min([pt[0] for pt in pts])), max(bbox[1], min([pt[1] for pt in pts])), min(bbox[2], max([pt[0] for pt in pts])), min(bbox[3], max([pt[1] for pt in pts]))]

    for y in range(bbox[1], bbox[3]):
        for x in range(bbox[0], bbox[2]):
            p = np.array([(x + 0.5) / width * (max_x - min_x) + min_x, (y + 0.5) / height * (max_y - min_y) + min_y])
            u, v, w = barycentric_coords(p, projected_triangle[0], projected_triangle[1], projected_triangle[2])
            if u >= 0 and v >= 0 and w >= 0:
                texture_color = get_texture_color(u * texture_triangle[0][0] + v * texture_triangle[1][0] + w * texture_triangle[2][0],
                                                  u * texture_triangle[0][1] + v * texture_triangle[1][1] + w * texture_triangle[2][1])
                image.putpixel((x, y), texture_color)

def painter_algorithm_textures(
        full_path_input_mesh,
        full_path_input_texture,
        full_path_output_image,
        min_x_coordinate_in_projection_plane,
        min_y_coordinate_in_projection_plane,
        max_x_coordinate_in_projection_plane,
        max_y_coordinate_in_projection_plane,
        width_in_pixels,
        height_in_pixels):
    
    vertices, texture_coords, faces = load_mesh(full_path_input_mesh)
    texture_image = Image.open(full_path_input_texture)
    
    triangles = [(vertices[face[0][0] - 1], vertices[face[1][0] - 1], vertices[face[2][0] - 1]) for face in faces]
    texture_triangles = [(texture_coords[face[0][1] - 1], texture_coords[face[1][1] - 1], texture_coords[face[2][1] - 1]) for face in faces]
    projected_triangles = [project_triangle(triangle) for triangle in triangles]
    
    distances = [max(np.linalg.norm(vertex) for vertex in triangle) for triangle in triangles]
    sorted_indices = np.argsort(distances)[::-1]  # Sort in descending order
    
    image = Image.new('RGB', (width_in_pixels, height_in_pixels), (0, 0, 0))
    
    for i in sorted_indices:
        triangle = triangles[i]
        projected_triangle = projected_triangles[i]
        texture_triangle = texture_triangles[i]
        draw_triangle(image, projected_triangle, texture_triangle, texture_image, min_x_coordinate_in_projection_plane, 
                      max_x_coordinate_in_projection_plane, min_y_coordinate_in_projection_plane, 
                      max_y_coordinate_in_projection_plane, width_in_pixels, height_in_pixels)
    
    image.save(full_path_output_image)

# Example usage
painter_algorithm_textures(
    full_path_input_mesh='sphere-rectangles.off',
    full_path_input_texture='texture2.png',
    full_path_output_image='photo-of-sphere.png',
    min_x_coordinate_in_projection_plane=-1.0,
    min_y_coordinate_in_projection_plane=-1.0,
    max_x_coordinate_in_projection_plane=1.0,
    max_y_coordinate_in_projection_plane=1.0,
    width_in_pixels=640,
    height_in_pixels=480
)
