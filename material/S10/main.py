import numpy as np

def create_cube():
    # Define the 8 vertices of the cube
    vertices = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ])

    # Define the 6 faces of the cube, each with 4 vertices
    faces = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5]
    ])

    # Define the texture coordinates for each vertex on each face
    texture_coords = np.array([
        [0, 0], [1, 0], [1, 1], [0, 1],  # Bottom face
        [0, 0], [1, 0], [1, 1], [0, 1],  # Top face
        [0, 0], [1, 0], [1, 1], [0, 1],  # Front face
        [0, 0], [1, 0], [1, 1], [0, 1],  # Back face
        [0, 0], [1, 0], [1, 1], [0, 1],  # Left face
        [0, 0], [1, 0], [1, 1], [0, 1],  # Right face
    ])
    
    return vertices, faces, texture_coords

def save_off_with_texture(filename, vertices, faces, texture_coords):
    with open(filename, 'w') as f:
        f.write('OFF\n')
        f.write(f'{len(vertices)} {len(faces)} 0\n')
        
        # Write vertices
        for vertex in vertices:
            f.write(f'{" ".join(map(str, vertex))}\n')
        
        # Write faces with texture coordinates
        for i, face in enumerate(faces):
            f.write(f'4 {" ".join(map(str, face))}')
            for j in range(4):
                tex_coord = texture_coords[i * 4 + j]
                f.write(f' {" ".join(map(str, tex_coord))}')
            f.write('\n')

# Generate cube data
vertices, faces, texture_coords = create_cube()

# Save the cube with texture information in OFF format
save_off_with_texture('cube_with_texture.off', vertices, faces, texture_coords)

print("OFF file with texture coordinates generated successfully.")



