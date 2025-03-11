import math

def sphere_with_quadrilateral_faces(full_path_output_file, radius, center):
    # Center of the sphere
    cx, cy, cz = center
    
    # Generate vertices on the sphere
    vertices = []
    for phi in range(0, 360, 1):
        for theta in range(0, 360, 1):
            phi_radians = math.radians(phi)
            theta_radians = math.radians(theta)
            x = cx + radius * math.sin(phi_radians) * math.cos(theta_radians)
            y = cy + radius * math.sin(phi_radians) * math.sin(theta_radians)
            z = cz + radius * math.cos(phi_radians)
            vertices.append((x, y, z))
    
    # Generate quadrilateral faces
    faces = []
    for phi in range(0, 359, 1):
        for theta in range(0, 359, 1):
            v1 = phi * 360 + theta
            v2 = phi * 360 + (theta + 1) % 360
            v3 = ((phi + 1) % 360) * 360 + (theta + 1) % 360
            v4 = ((phi + 1) % 360) * 360 + theta
            faces.append((v1, v2, v3, v4))
    
    # Determine file extension
    extension = full_path_output_file.split('.')[-1].lower()
    
    # Write to file based on file format
    if extension == 'off':
        with open(full_path_output_file, 'w') as file:
            file.write('OFF\n')
            file.write(f'{len(vertices)} {len(faces)} 0\n')
            for vertex in vertices:
                file.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')
            for face in faces:
                file.write(f'4 {face[0]} {face[1]} {face[2]} {face[3]}\n')
    
    elif extension == 'ply':
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
                file.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')
            for face in faces:
                file.write(f'4 {face[0]} {face[1]} {face[2]} {face[3]}\n')
    
    else:
        raise ValueError("Unsupported file extension. Please use either 'off' or 'ply'.")

sphere_with_quadrilateral_faces(
    full_path_output_file = 'sphere-rectangles.off',
    radius = 5,
    center = (2,3,5)
)

sphere_with_quadrilateral_faces(
    full_path_output_file = 'sphere-rectangles.ply',
    radius = 5,
    center = (2,3,5)
)

