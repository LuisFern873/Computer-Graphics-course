import cv2
import numpy as np

def load_off(filename):
    with open(filename, 'r') as f:
        header = f.readline().strip()
        
        if header not in ["OFF", "STOFF", "NOFF"]:
            raise ValueError("El archivo no está en formato OFF válido")
        
        # Leer número de vértices y caras
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


def project_points(points, K, R, t):
    projected_points = []
    for point in points:
        world_point = np.dot(R, point) + t
        image_point = np.dot(K, world_point)
        image_point /= image_point[2]  # Normalize
        projected_points.append(image_point[:2])
    return np.array(projected_points, dtype=np.int32)

def draw_mesh_on_top_of_marker(full_path_input_image, full_path_mesh, full_path_output_image):

    marker_image = cv2.imread('exercise03/marker.png', cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    kp_marker, des_marker = orb.detectAndCompute(marker_image, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    frame = cv2.imread(full_path_input_image)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)
    matches = bf.match(des_marker, des_frame)

    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > 85:
        src_pts = np.float32([kp_marker[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = marker_image.shape
        pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, matrix)
        frame = cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 3)

        mesh_vertices, _ = load_off(full_path_mesh)

        # Definir parámetros de la cámara (estos deben ajustarse según la cámara utilizada)
        K = np.array([[800, 0, frame.shape[1] // 2], [0, 800, frame.shape[0] // 2], [0, 0, 1]])
        R = np.eye(3)  # Suponiendo que el marcador está en un plano


        # Ajustar la profundidad según el modelo
        mesh_size = np.max(mesh_vertices, axis=0) - np.min(mesh_vertices, axis=0)
        scale_factor = np.linalg.norm(mesh_size)  # Tamaño global del mesh
        t_z = -10 * (scale_factor / 10)  # Ajusta el factor base (10 en este caso)
        t = np.array([0, 0, t_z])

        projected_vertices = project_points(mesh_vertices, K, R, t)

        # Dibujar el mesh
        for vertex in projected_vertices:
            cv2.circle(frame, tuple(vertex), 1, (0, 0, 255), -1)

    cv2.imwrite(full_path_output_image, frame)

# Based on:
# https://chatgpt.com/c/67d78a56-f41c-800b-aa9a-23ee6458db83
