import numpy as np
import math

def parse_off(file_path):
    with open(file_path, 'r') as file:
        if 'OFF' != file.readline().strip():
            raise ValueError('Not a valid OFF header')
        n_verts, n_faces, n_edges = map(int, file.readline().strip().split())
        verts = []
        for _ in range(n_verts):
            verts.append(list(map(float, file.readline().strip().split())))
        faces = []
        for _ in range(n_faces):
            faces.append(list(map(int, file.readline().strip().split())))
    return np.array(verts), faces

def write_off(file_path, verts, faces):
    with open(file_path, 'w') as file:
        file.write('OFF\n')
        file.write(f'{len(verts)} {len(faces)} 0\n')
        for vert in verts:
            file.write(' '.join(map(str, vert)) + '\n')
        for face in faces:
            file.write(' '.join(map(str, face)) + '\n')

def parse_ply(file_path):
    with open(file_path, 'r') as file:
        if 'ply' != file.readline().strip():
            raise ValueError('Not a valid PLY header')
        while 'end_header' not in file.readline().strip():
            continue
        verts = []
        while True:
            line = file.readline().strip()
            if line == '':
                break
            verts.append(list(map(float, line.split())))
        faces = []
        for line in file:
            faces.append(list(map(int, line.strip().split())))
    return np.array(verts), faces

def write_ply(file_path, verts, faces):
    with open(file_path, 'w') as file:
        file.write('ply\n')
        file.write('format ascii 1.0\n')
        file.write(f'element vertex {len(verts)}\n')
        file.write('property float x\n')
        file.write('property float y\n')
        file.write('property float z\n')
        file.write(f'element face {len(faces)}\n')
        file.write('property list uchar int vertex_index\n')
        file.write('end_header\n')
        for vert in verts:
            file.write(' '.join(map(str, vert)) + '\n')
        for face in faces:
            file.write(' '.join(map(str, face)) + '\n')

def rotation_matrix(axis, theta):
    axis = np.array(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotate_mesh_around_line(full_path_input_mesh, axis_of_rotation, angle, full_path_output_mesh):
    if full_path_input_mesh.endswith('.off'):
        verts, faces = parse_off(full_path_input_mesh)
        write_mesh = write_off
    elif full_path_input_mesh.endswith('.ply'):
        verts, faces = parse_ply(full_path_input_mesh)
        write_mesh = write_ply
    else:
        raise ValueError('Unsupported file format')
    
    (px, py, pz), (dx, dy, dz) = axis_of_rotation
    axis = (dx, dy, dz)
    theta = math.radians(angle)
    R = rotation_matrix(axis, theta)
    
    rotated_verts = []
    for vert in verts:
        vert = np.array(vert) - np.array([px, py, pz])
        rotated_vert = np.dot(R, vert)
        rotated_vert = rotated_vert + np.array([px, py, pz])
        rotated_verts.append(rotated_vert)
    
    write_mesh(full_path_output_mesh, rotated_verts, faces)

# TEST CASES
rotate_mesh_around_line(
    full_path_input_mesh = 'cube.off',
    axis_of_rotation = ((0,0,0),(0,0,1)),
    angle = 35,
    full_path_output_mesh='cube-rotated.off'
)

# rotate_mesh_around_line(
#     full_path_input_mesh = 'sphere-rectangles.ply',
#     axis_of_rotation = ((0,0,0),(0,0,1)),
#     angle = 35,
#     full_path_output_mesh='sphere-rectangles-rotated.ply'
# )