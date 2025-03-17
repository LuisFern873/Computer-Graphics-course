import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def load_off(filename):
    with open(filename, 'r') as f:
        if 'OFF' not in f.readline():
            raise ValueError("Not a valid OFF file")
        
        num_vertices, num_faces, _ = map(int, f.readline().strip().split())
        vertices = [list(map(float, f.readline().strip().split())) for _ in range(num_vertices)]
        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(num_faces)]
        
    return np.array(vertices), faces

def compute_depth(face, vertices):
    return np.mean([vertices[i][2] for i in face])  # Promedio de la coordenada Z

def sort_faces_by_depth(faces, vertices):
    return sorted(faces, key=lambda face: compute_depth(face, vertices), reverse=True)

def plot_mesh(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    sorted_faces = sort_faces_by_depth(faces, vertices)
    
    for face in sorted_faces:
        poly = [vertices[i] for i in face]
        ax.add_collection3d(Poly3DCollection([poly], alpha=0.5, edgecolor='k'))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Cargar y visualizar archivo OFF
off_file = "./exercise12/icosahedron.off"  # Reemplázalo con el nombre del archivo
vertices, faces = load_off(off_file)
plot_mesh(vertices, faces)
