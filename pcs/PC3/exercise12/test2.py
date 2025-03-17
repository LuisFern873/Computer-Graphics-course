import numpy as np
import cv2
import matplotlib.pyplot as plt

def load_off(filename):
    with open(filename, 'r') as f:
        if f.readline().strip() != "OFF":
            raise ValueError("El archivo no está en formato OFF")
        
        n_verts, n_faces, _ = map(int, f.readline().strip().split())
        
        # Leer vértices
        vertices = np.array([list(map(float, f.readline().strip().split())) for _ in range(n_verts)], dtype=np.float32)
        
        # Leer caras
        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(n_faces)]
        
        return vertices, faces

def project_3d_to_2d(vertices, K, rvec, tvec):
    points_2D, _ = cv2.projectPoints(vertices, rvec, tvec, K, distCoeffs=None)
    return points_2D.reshape(-1, 2)

# Cargar archivo OFF
filename = "./exercise12/bunny_simple.off"  # Cambia esto por el path de tu archivo
vertices_3D, faces = load_off(filename)

# Definir la matriz intrínseca de la Pinhole Camera
fx, fy = 800, 800  # Focal en píxeles
cx, cy = 320, 240  # Centro óptico (para una imagen 640x480)
K = np.array([[fx, 0, cx], [0, fy, cy], [0,  0,  1]], dtype=np.float32)

# Definir la rotación y traslación de la cámara
rvec = np.zeros((3, 1))  # Sin rotación
tvec = np.array([[0], [0], [-3]], dtype=np.float32)  # Traslación en Z

# Proyectar puntos 3D a 2D
vertices_2D = project_3d_to_2d(vertices_3D, K, rvec, tvec)

# Visualizar proyección
plt.figure(figsize=(6, 6))
plt.scatter(vertices_2D[:, 0], -vertices_2D[:, 1], s=1, color='blue')  # Invertir Y para que se vea correctamente

# Dibujar aristas
for face in faces:
    for i in range(len(face)):
        v1 = vertices_2D[face[i]]
        v2 = vertices_2D[face[(i+1) % len(face)]]  # Conectar con el siguiente vértice
        plt.plot([v1[0], v2[0]], [-v1[1], -v2[1]], color='black', linewidth=0.5)

plt.xlim(0, 640)
plt.ylim(-480, 0)
plt.gca().invert_yaxis()
plt.title("Proyección 2D del Mesh con Aristas")
plt.show()


