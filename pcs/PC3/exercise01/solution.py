
def cube_with_square_faces(full_path_output_file):
    vertices = [
        [-1, -1, -1], # A: 0
        [-1,  1, -1], # B: 1
        [-1,  1,  1], # C: 2
        [-1, -1,  1], # D: 3    
        [ 1, -1, -1], # E: 4
        [ 1,  1, -1], # F: 5
        [ 1,  1,  1], # G: 6
        [ 1, -1,  1]  # H: 7
    ]

    faces = [
        [0, 3, 2, 1],
        [3, 7, 6, 2],
        [7, 4, 5, 6],
        [4, 0, 1, 5],
        [1, 2, 6, 5],
        [3, 0, 4, 7]
    ]

    file_extension = full_path_output_file.split('.')[-1].lower()

    if file_extension == 'off':
        with open(full_path_output_file, 'w') as file:
            file.write('OFF\n')
            file.write(f'{len(vertices)} {len(faces)} 0\n')
            for vertex in vertices:
                file.write(f'{" ".join(map(str, vertex))}\n')
            for face in faces:
                file.write(f'{" ".join(map(str, [len(face)] + face))}\n')

    elif file_extension == 'ply':
        with open(full_path_output_file, 'w') as file:
            file.write('ply\n')
            file.write('format ascii 1.0\n')
            file.write(f'element vertex {len(vertices)}\n')
            file.write('property float x\n')
            file.write('property float y\n')
            file.write('property float z\n')
            file.write(f'element face {len(faces)}\n')
            file.write('property list uchar int vertex_indices\n')
            file.write('end_header\n')
            for vertex in vertices:
                file.write(f'{" ".join(map(str, vertex))}\n')
            for face in faces:
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')

    else:
        raise ValueError("Unsupported file extension. Please use either 'off' or 'ply'.")

cube_with_square_faces(
    full_path_output_file = "cube.off"
)
cube_with_square_faces(
    full_path_output_file = "cube.ply"
)



