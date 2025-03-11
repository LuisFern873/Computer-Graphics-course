import numpy as np

def read_off(file_path):
    with open(file_path, 'r') as file:
        header = file.readline().strip()
        if header != 'OFF':
            raise ValueError("Not a valid OFF file")
        
        counts = file.readline().strip().split()
        num_vertices = int(counts[0])
        num_faces = int(counts[1])
        num_edges = int(counts[2])

        vertices = []
        for _ in range(num_vertices):
            vertex = list(map(float, file.readline().strip().split()))
            vertices.append(vertex)

        faces = []
        for _ in range(num_faces):
            face = list(map(int, file.readline().strip().split()))
            faces.append(face)

    return vertices, faces

# For each face, add a face point
    # Set each face point to be the average of all original points for the respective face
def compute_face_points(faces, vertices):
    face_points = []
    for face in faces:
        # n: number of vertices of the face
        n = face[0]
        face_point = [0, 0, 0]
        for i in range(1, n + 1):
            index = face[i] # vertex index
            vertex = vertices[index] # vertex [x, y, z]
            face_point[0] += vertex[0] 
            face_point[1] += vertex[1] 
            face_point[2] += vertex[2]
        face_point[0] /= n
        face_point[1] /= n
        face_point[2] /= n
        face_points.append(face_point)
    return face_points

def identify_edges(faces):
    edges = {}
    for j in range(len(faces)):
        n = faces[j][0]
        indices = faces[j][1:]
        for i in range(n):
            v1 = indices[i]
            v2 = indices[(i + 1) % n]
            edge = (min(v1, v2), max(v1, v2))
            if edge in edges:
                edges[edge].append(j)
            else:
                edges[edge] = [j]
    return edges

# For each edge, add an edge point.
# Set each edge point to be the average of the two neighbouring face points (A,F) and the two endpoints of the edge (M,E) 
# (𝐴+𝐹+𝑀+𝐸) / 4

def compute_edge_points(faces, face_points, vertices):
    edge_points = []
    # Identify edges and neighbor faces!
    edges = identify_edges(faces)
    # (v1, v2) = [f1, f2]
    for edge, neighbor_face in edges.items():
        v1, v2 = edge
        f1, f2 = neighbor_face
        M, E = vertices[v1], vertices[v2]
        A, F = face_points[f1], face_points[f2]
        edge_point = [
            (M[0] + E[0] + A[0] + F[0]) / 4,
            (M[1] + E[1] + A[1] + F[1]) / 4,
            (M[2] + E[2] + A[2] + F[2]) / 4
        ]
        edge_points.append(edge_point)
    return edge_points

def compute_new_vertices(faces, face_points, vertices):
    # Identify neighbor faces (touch it)
    # Identify neighbor vertices (touch it)
    dict_neighbor_faces = {} # point index : [neighbor faces indices]
    dict_neighbor_vertices = {} # point index : [neighbor edges indices]
    for j in range(len(faces)):
        n = faces[j][0]
        indices = faces[j][1:]
        for i in range(len(indices)): # point i
            if indices[i] in dict_neighbor_faces:
                dict_neighbor_faces[indices[i]].append(j)
            else:
                dict_neighbor_faces[indices[i]] = [j]
            if indices[i] in dict_neighbor_vertices:
                dict_neighbor_vertices[indices[i]].append(indices[(i + 1) % n])
            else:
                dict_neighbor_vertices[indices[i]] = [indices[(i + 1) % n]]

    for (point, neighbor_faces), (_, neighbor_vertices) in zip(dict_neighbor_faces.items(), dict_neighbor_vertices.items()):
        print ("Point = ", point)
        n = len(neighbor_faces)
        Fpoint = [0, 0, 0]
        for face in neighbor_faces: # face index
            Fpoint[0] += face_points[face][0]
            Fpoint[1] += face_points[face][1]
            Fpoint[2] += face_points[face][2]
        Fpoint[0] /= n
        Fpoint[1] /= n
        Fpoint[2] /= n

        print("Fpoint = ", Fpoint)

        average_points = []
        p1 = np.array(vertices[point])
        for vertex in neighbor_vertices:
            p2 = np.array(vertices[vertex])
            average_point = (p1 + p2) / 2
            average_points.append(average_point)
        
        Rpoint = np.mean(average_points, axis=0)
        print("Rpoint = ", Rpoint)

        new_vertex = (np.array(Rpoint) + 2 * np.array(Rpoint) + (n - 3)* np.array(vertices[point])) / n
        print("New vertex = ", new_vertex) # replace this vertex for the original
            

    return dict_neighbor_faces

# Usage example
file_path = 'cube.off'
vertices, faces = read_off(file_path)

face_points = compute_face_points(faces, vertices)
edge_points = compute_edge_points(faces, face_points, vertices)

print("Face points: ", face_points)
print("Edge points: ", edge_points)

# print("Hello: ", )
compute_new_vertices(faces, face_points, vertices)
