from plyfile import PlyData, PlyElement
import numpy as np
import math

# pip install plyfile

def read_ply(filename):
    ply_data = PlyData.read(filename)
    vertices = np.array([list(vertex) for vertex in ply_data['vertex']])
    return vertices, ply_data

def compute_texture_coordinates(vertices, center):
    texture_coordinates = []
    for vertex in vertices:
        vx, vy, vz = vertex[:3] - center
        theta = math.atan2(vy, vx)
        phi = math.acos(vz / np.linalg.norm([vx, vy, vz]))
        
        u = (theta + math.pi) / (2 * math.pi)
        v = phi / math.pi
        texture_coordinates.append([u, v])
    return np.array(texture_coordinates)

def write_ply(vertices, texture_coordinates, ply_data, output_filename):
    vertex_data = []
    for i in range(len(vertices)):
        vertex_data.append((*vertices[i], *texture_coordinates[i]))

    vertex_element = PlyElement.describe(np.array(vertex_data, dtype=[
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('u', 'f4'), ('v', 'f4')
    ]), 'vertex')

    PlyData([vertex_element, *ply_data.elements[1:]]).write(output_filename)

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    vertices, ply_data = read_ply(full_path_input_ply)
    texture_coordinates = compute_texture_coordinates(vertices, center)
    write_ply(vertices, texture_coordinates, ply_data, full_path_output_ply)

sphere_with_texture('input.ply', 'texture2.png', [0, 0, 0], 'output.ply')

