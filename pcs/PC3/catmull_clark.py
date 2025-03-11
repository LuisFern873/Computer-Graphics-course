import sys
from collections import defaultdict

def read_off(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    assert lines[0].strip() == "OFF", "El archivo no está en formato OFF"
    
    v_count, f_count, _ = map(int, lines[1].split())
    
    vertices = [list(map(float, line.split())) for line in lines[2:2 + v_count]]
    faces = [list(map(int, line.split()[1:])) for line in lines[2 + v_count:2 + v_count + f_count]]
    
    return vertices, faces

def compute_face_points(vertices, faces):
    face_points = []
    for face in faces:
        avg_x = sum(vertices[v][0] for v in face) / len(face)
        avg_y = sum(vertices[v][1] for v in face) / len(face)
        avg_z = sum(vertices[v][2] for v in face) / len(face)
        face_points.append([avg_x, avg_y, avg_z])
    return face_points

def compute_edge_points(vertices, faces, face_points):

    edge_dict = defaultdict(list)

    # Construir diccionario de aristas con sus caras adyacentes
    for i, face in enumerate(faces):
        num_vertices = len(face)
        for j in range(num_vertices):
            v_a, v_b = face[j], face[(j + 1) % num_vertices]
            edge = tuple(sorted((v_a, v_b)))  # Asegurar orden para evitar duplicados
            edge_dict[edge].append(i)

    edge_points = {}
    
    for edge, face_list in edge_dict.items():
        v_a, v_b = edge
        mid_x = (vertices[v_a][0] + vertices[v_b][0]) / 2
        mid_y = (vertices[v_a][1] + vertices[v_b][1]) / 2
        mid_z = (vertices[v_a][2] + vertices[v_b][2]) / 2

        if len(face_list) == 2: # Arista con dos caras adyacentes (F1 y F2)
            f1, f2 = face_list
            f1_x, f1_y, f1_z = face_points[f1]
            f2_x, f2_y, f2_z = face_points[f2]
            edge_x = (mid_x + f1_x + f2_x) / 3
            edge_y = (mid_y + f1_y + f2_y) / 3
            edge_z = (mid_z + f1_z + f2_z) / 3
        else: # Arista en frontera (solo un Face Point)
            f1 = face_list[0]
            f1_x, f1_y, f1_z = face_points[f1]
            edge_x = (mid_x + f1_x) / 2
            edge_y = (mid_y + f1_y) / 2
            edge_z = (mid_z + f1_z) / 2

        edge_points[edge] = [edge_x, edge_y, edge_z]

    return edge_points

def compute_new_vertices(vertices, faces, face_points, edge_points):

    vertex_faces = defaultdict(list)
    vertex_edges = defaultdict(list)

    for i, face in enumerate(faces):
        for j, v in enumerate(face):
            vertex_faces[v].append(i)
            edge = tuple(sorted((v, face[(j + 1) % len(face)])))
            vertex_edges[v].append(edge)

    new_vertices = []
    
    for i, vertex in enumerate(vertices):
        F = [face_points[f] for f in vertex_faces[i]]
        R = [edge_points[e] for e in vertex_edges[i]]

        avg_F = [sum(f[j] for f in F) / len(F) for j in range(3)]
        avg_R = [sum(r[j] for r in R) / len(R) for j in range(3)]

        new_x = (avg_F[0] + 2 * avg_R[0] + vertex[0]) / 4
        new_y = (avg_F[1] + 2 * avg_R[1] + vertex[1]) / 4
        new_z = (avg_F[2] + 2 * avg_R[2] + vertex[2]) / 4

        new_vertices.append([new_x, new_y, new_z])

    return new_vertices

def create_new_faces(faces, face_points, edge_points, vertex_offset):

    new_faces = []
    face_offset = len(vertex_offset)
    edge_offset = face_offset + len(face_points)

    edge_map = {edge: i + edge_offset for i, edge in enumerate(edge_points)}

    for i, face in enumerate(faces):
        face_center = face_offset + i
        num_v = len(face)

        for j in range(num_v):
            v1, v2 = face[j], face[(j + 1) % num_v]
            e1 = edge_map[tuple(sorted((v1, v2)))]
            e2 = edge_map[tuple(sorted((face[j - 1], v1)))]

            new_faces.append([v1, e1, face_center, e2])

    return new_faces

def write_off(filename, vertices, faces):

    with open(filename, 'w') as file:
        file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")
        
        for v in vertices:
            file.write(f"{v[0]} {v[1]} {v[2]}\n")
        
        for face in faces:
            file.write(f"{len(face)} {' '.join(map(str, face))}\n")

def catmull_clark(input_file, number_of_iterations, output_file):
    vertices, faces = read_off(input_file)

    for _ in range(number_of_iterations):
        face_points = compute_face_points(vertices, faces)
        edge_points = compute_edge_points(vertices, faces, face_points)
        new_vertices = compute_new_vertices(vertices, faces, face_points, edge_points)
        new_faces = create_new_faces(faces, face_points, edge_points, vertices)

        vertices = new_vertices + face_points + list(edge_points.values())
        faces = new_faces

    write_off(output_file, vertices, faces)
    print(f"Archivo generado: {output_file}")

if __name__ == "__main__":

    # test case 1 
    catmull_clark("./meshes/dodecahedron.off", 1, "./meshes/dodecahedron_prime.off")

    # test case 2
    catmull_clark("./meshes/cube4.off", 3, "./meshes/cube4_prime.off")
    