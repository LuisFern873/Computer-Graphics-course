import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_off(filename):
    with open(filename, 'r') as f:
        header = f.readline().strip()
        
        if header not in ["OFF", "STOFF", "NOFF"]:
            raise ValueError("El archivo no está en formato OFF válido")
        
        while True:
            line = f.readline().strip()
            if not line.startswith('#'):
                n_verts, n_faces, _ = map(int, line.split())
                break

        vertices = []
        for _ in range(n_verts):
            while True:
                line = f.readline().strip()
                if not line.startswith('#'):
                    values = list(map(float, line.split()))
                    
                    # Manejo de NOFF y STOFF
                    if header == "NOFF":
                        vertex_data = values[:3]  # Solo las coordenadas
                        color_data = values[3:]  # Ignorar los colores
                    elif header == "STOFF":
                        vertex_data = values[:3]  # Solo coordenadas
                        scale_data = values[3:]   # Ignorar la escala
                    else:
                        vertex_data = values
                    
                    vertices.append(vertex_data)
                    break

        faces = []
        for _ in range(n_faces):
            while True:
                line = f.readline().strip()
                if not line.startswith('#'):
                    face_data = list(map(int, line.split()[1:]))  # Ignorar primer valor (número de vértices)
                    faces.append(face_data)
                    break

        return np.array(vertices, dtype=np.float32), faces

def project_3d_to_2d(vertices, K, rvec, tvec):
    points_2D, _ = cv2.projectPoints(vertices, rvec, tvec, K, distCoeffs=None)
    return points_2D.reshape(-1, 2)

# Doubt: Where should I use the optical_center_z parameter?
def sequence_of_projections(
    full_path_input_mesh,
    optical_center_x, optical_center_y, optical_center_z,
    optical_axis_x, optical_axis_y, optical_axis_z, 
    focal_distance,
    output_width_in_pixels, 
    output_height_in_pixels,
    prefix_output_files
):
    vertices_3D, _ = load_off(full_path_input_mesh)

    frames = len(optical_center_x)

    for i in range(frames):

        fx, fy = focal_distance[i], focal_distance[i]
        cx, cy = optical_center_x[i], optical_center_y[i]

        # Calibration matrix (intrinsic parameters)
        K = np.array([[fx, 0, cx], [0, fy, cy], [0,  0,  1]], dtype=np.float32)

        # Extrinsic parameters (no rotation)
        rvec = np.zeros((3, 1))
        tvec = np.array([[optical_axis_x[i]], [optical_axis_y[i]], [optical_axis_z[i]]], dtype=np.float32)

        vertices_2D = project_3d_to_2d(vertices_3D, K, rvec, tvec)

        plt.figure(figsize=(6, 6))
        plt.scatter(vertices_2D[:, 0], -vertices_2D[:, 1], s=1, color='green')

        plt.xlim(0, output_width_in_pixels)
        plt.ylim(-output_height_in_pixels, 0)
        # plt.gca().invert_yaxis()
        plt.savefig(f"{prefix_output_files}-{i + 1}.png")
        print(f"{prefix_output_files}-{i + 1}.png generated.")

