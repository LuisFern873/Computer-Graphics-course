import numpy as np
import matplotlib.pyplot as plt

def load_off(file_path):
    """Load an OFF file and return vertices and faces."""
    with open(file_path, 'r') as f:
        if f.readline().strip() != 'OFF':
            raise ValueError("Not a valid OFF file")
        
        num_vertices, num_faces, _ = map(int, f.readline().split())
        vertices = np.array([list(map(float, f.readline().split())) for _ in range(num_vertices)])
        faces = [list(map(int, f.readline().split()[1:])) for _ in range(num_faces)]
        
    return vertices, faces

def project_orthographic(vertices):
    """Orthographic projection (ignores z-axis)."""
    return vertices[:, :2]  # Keep only x and y

def draw_and_save_mesh(vertices, faces, output_path="output.png"):
    """Draw the 2D projection of the mesh and save it as a PNG."""
    projected_vertices = project_orthographic(vertices)
    
    fig, ax = plt.subplots(figsize=(6,6))
    
    # Draw edges of the mesh
    for face in faces:
        polygon = projected_vertices[face]
        polygon = np.vstack([polygon, polygon[0]])  # Close the loop
        ax.plot(polygon[:, 0], polygon[:, 1], 'k-', linewidth=1)
    
    # Plot vertices
    ax.scatter(projected_vertices[:, 0], projected_vertices[:, 1], c='red', s=5)  
    
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes for a clean output
    
    # Save the figure as a PNG
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

off_file = "./exercise12/icosahedron.off"
vertices, faces = load_off(off_file)
draw_and_save_mesh(vertices, faces, "./exercise12/icosahedron.png")

