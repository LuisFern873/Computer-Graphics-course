import numpy as np
from PIL import Image
from math import atan2, acos, pi

def read_ply(file_path):
    vertices = []
    faces = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        vertex_section = False
        face_section = False
        
        for line in lines:
            if line.startswith('end_header'):
                vertex_section = True
                continue
            
            if vertex_section:
                vertex_info = line.split()
                if len(vertex_info) == 3:
                    vertices.append([float(vertex_info[0]), float(vertex_info[1]), float(vertex_info[2])])
            
            if line.startswith('3'):
                face_info = line.split()
                if len(face_info) == 4:  # assuming triangles
                    faces.append([int(face_info[1]), int(face_info[2]), int(face_info[3])])
    
    return np.array(vertices), np.array(faces)

def write_ply(vertices, faces, texture_coords, output_file):
    with open(output_file, 'w') as f:
        # Write header
        f.write('ply\n')
        f.write('format ascii 1.0\n')
        f.write('element vertex {}\n'.format(len(vertices)))
        f.write('property float x\n')
        f.write('property float y\n')
        f.write('property float z\n')
        f.write('element face {}\n'.format(len(faces)))
        f.write('property list uchar int vertex_indices\n')
        f.write('end_header\n')
        
        # Write vertices
        for i in range(len(vertices)):
            f.write('{} {} {} {} {}\n'.format(vertices[i][0], vertices[i][1], vertices[i][2], texture_coords[i][0], texture_coords[i][1]))
        
        # Write faces
        for face in faces:
            f.write('3 {} {} {}\n'.format(face[0], face[1], face[2]))

def compute_texture_coordinates(vertices, center):
    texture_coords = []
    for v in vertices:
        # Compute polar coordinates relative to center
        vec_to_vertex = v - center
        theta = atan2(vec_to_vertex[1], vec_to_vertex[0])
        phi = acos(vec_to_vertex[2] / np.linalg.norm(vec_to_vertex))
        
        # Map to texture coordinates (u, v)
        u = (theta + pi) / (2 * pi)  # Normalize theta to [0, 1]
        v = phi / pi                  # Normalize phi to [0, 1]
        
        texture_coords.append([u, v])
    
    return np.array(texture_coords)

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    # Read the input PLY file
    vertices, faces = read_ply(full_path_input_ply)
    
    # Compute texture coordinates
    texture_coords = compute_texture_coordinates(vertices, center)
    
    # Write the modified PLY file with texture coordinates
    write_ply(vertices, faces, texture_coords, full_path_output_ply)

# Example usage:
full_path_input_ply = 'sphere-rectangles.ply'
full_path_texture = 'texture2.png'
center = np.array([0, 0, 0])  # Center of the sphere
full_path_output_ply = 'sphere-rectangles-with-texture.ply'

sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply)


# sphere_with_texture(
#     full_path_input_ply='/home/someone/sphere-rectangles.ply',
#     full_path_texture='texture1.png',
# center=(2,3,5),
# full_path_output_ply='sphere-with-texture-1.ply')
