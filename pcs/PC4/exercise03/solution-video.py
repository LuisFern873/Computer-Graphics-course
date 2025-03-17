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


vertices, faces = load_off('./meshes-for-exercises-1-2-3/bunny.off')

# vertices, faces = load_off('./meshes-for-exercises-1-2-3/gargoyle-10k-faces.off')


marker_image = cv2.imread('./exercise03/marker.png', cv2.IMREAD_GRAYSCALE)
orb = cv2.ORB_create()
kp_marker, des_marker = orb.detectAndCompute(marker_image, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)
    matches = bf.match(des_marker, des_frame)
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > 135:
        # Calcular homografía
        src_pts = np.float32([kp_marker[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)


        transformed_vertices = []
        for v in vertices:
            v_2d = np.dot(matrix, np.array([v[0], v[1], 1]))  # 2D projection
            transformed_vertices.append([v_2d[0] / v_2d[2], v_2d[1] / v_2d[2]])

        transformed_vertices = np.array(transformed_vertices, dtype=np.int32)


        # Draw mesh faces!
        for face in faces:
            pts = np.array([transformed_vertices[i] for i in face], np.int32)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=1)

    cv2.imshow('AR Mesh', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

