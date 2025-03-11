import numpy as np

def read_off(file_path):
    with open(file_path, 'r') as file:
        if 'OFF' != file.readline().strip():
            raise ValueError('Not a valid OFF header')
        
        n_verts, n_faces, n_edges = map(int, file.readline().strip().split())
        
        verts = [list(map(float, file.readline().strip().split())) for _ in range(n_verts)]
        
        faces = [list(map(int, file.readline().strip().split()))[1:] for _ in range(n_faces)]
        
        return np.array(verts), faces

def write_off(file_path, verts, faces):
    with open(file_path, 'w') as file:
        file.write('OFF\n')
        file.write(f'{len(verts)} {len(faces)} 0\n')
        for vert in verts:
            file.write(' '.join(map(str, vert)) + '\n')
        for face in faces:
            file.write(f'{len(face)} ' + ' '.join(map(str, face)) + '\n')

def read_ply(file_path):
    with open(file_path, 'r') as file:
        if 'ply' != file.readline().strip():
            raise ValueError('Not a valid PLY header')
        
        n_verts = n_faces = 0
        while True:
            line = file.readline().strip()
            if line.startswith('element vertex'):
                n_verts = int(line.split()[-1])
            elif line.startswith('element face'):
                n_faces = int(line.split()[-1])
            elif line == 'end_header':
                break
        
        verts = [list(map(float, file.readline().strip().split())) for _ in range(n_verts)]
        
        faces = [list(map(int, file.readline().strip().split()))[1:] for _ in range(n_faces)]
        
        return np.array(verts), faces

def write_ply(file_path, verts, faces):
    with open(file_path, 'w') as file:
        file.write('ply\nformat ascii 1.0\n')
        file.write(f'element vertex {len(verts)}\n')
        file.write('property float x\nproperty float y\nproperty float z\n')
        file.write(f'element face {len(faces)}\n')
        file.write('property list uchar int vertex_indices\n')
        file.write('end_header\n')
        for vert in verts:
            file.write(' '.join(map(str, vert)) + '\n')
        for face in faces:
            file.write(f'{len(face)} ' + ' '.join(map(str, face)) + '\n')

def translate_mesh(full_path_input_mesh, d, full_path_output_mesh):
    d_x, d_y, d_z = d
    if full_path_input_mesh.endswith('.off'):
        verts, faces = read_off(full_path_input_mesh)
        verts += np.array([d_x, d_y, d_z])
        write_off(full_path_output_mesh, verts, faces)
    elif full_path_input_mesh.endswith('.ply'):
        verts, faces = read_ply(full_path_input_mesh)
        verts += np.array([d_x, d_y, d_z])
        write_ply(full_path_output_mesh, verts, faces)
    else:
        raise ValueError('Unsupported file format')

translate_mesh('cube.off', (1.0, 2.0, 3.0), 'translated-cube.off')