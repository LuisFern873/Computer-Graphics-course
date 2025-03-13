import numpy as np

def read_off(filename):
    with open(filename, 'r') as f:
        if 'OFF' != f.readline().strip():
            raise ValueError("Not a valid OFF file")
        n_verts, n_faces, _ = map(int, f.readline().strip().split())
        vertices = [list(map(float, f.readline().strip().split())) for _ in range(n_verts)]
        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(n_faces)]
    return np.array(vertices), faces

def write_off(filename, vertices, faces):

    with open(filename, 'w') as file:
        file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")
        
        for v in vertices:
            file.write(f"{v[0]} {v[1]} {v[2]}\n")
        
        for face in faces:
            file.write(f"{len(face)} {' '.join(map(str, face))}\n")

def loop_subdivision(vertices, faces):
    edge_map = {}
    new_vertices = list(vertices)
    new_faces = []
    edge_points = {}
    
    for face in faces: # v1, v2, v3
        for i in range(3):
            edge = tuple(sorted([face[i], face[(i+1)%3]]))
            if edge not in edge_points:
                v1, v2 = vertices[edge[0]], vertices[edge[1]]
                edge_points[edge] = (15/16) * (v1 + v2)
                edge_map[edge] = len(new_vertices)
                new_vertices.append(edge_points[edge])
    
    for i, v in enumerate(vertices):
        n = sum(1 for face in faces for j in range(3) if face[j] == i)
        beta = (15/16 - (15/16) * (n if n > 3 else 3)) / n
        neighbors = np.sum([vertices[j] for face in faces for j in face if i in face and j != i], axis=0)
        new_vertices[i] = (1 - n * beta) * v + beta * neighbors
    
    for face in faces:
        a, b, c = face
        ab, bc, ca = edge_map[(min(a, b), max(a, b))], edge_map[(min(b, c), max(b, c))], edge_map[(min(c, a), max(c, a))]
        new_faces.extend([[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]])
    
    return np.array(new_vertices), new_faces


def loop(input_file, number_of_iterations, output_file):

    vertices, faces = read_off(input_file)

    for _ in range(number_of_iterations):
        vertices, faces = loop_subdivision(vertices, faces)

    write_off(output_file, vertices, faces)
    print(f"Archivo generado: {output_file}")

    pass

if __name__ == "__main__":

    loop("./meshes/icosahedron.off", 1, "./meshes/icosahedron_loop_1.off")
    loop("./meshes/icosahedron.off", 2, "./meshes/icosahedron_loop_2.off")


