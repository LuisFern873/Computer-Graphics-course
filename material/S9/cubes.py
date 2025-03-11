import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from skimage import measure

# By: Luis Méndez 

def draw_surface(function, output_file, min_x, min_y, min_z, max_x, max_y, max_z):

    x = np.arange(min_x, max_x + 1, 1)
    y = np.arange(min_y, max_y + 1, 1)
    z = np.arange(min_z, max_z + 1, 1)
    x, y, z = np.meshgrid(x, y, z)

    values = function(x, y, z)

    verts, faces, _, _ = measure.marching_cubes(values, level=0.5) # , spacing=(20/21, 20/21, 20/21)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the isosurface
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2],
                    cmap='Spectral', lw=1, edgecolor='none')

    ax.set_xlim(0, abs(min_x) + abs(max_x))
    ax.set_ylim(0, abs(min_y) + abs(max_y))
    ax.set_zlim(0, abs(min_z) + abs(max_z))
    plt.show()
    plt.savefig(output_file, format='eps')
    plt.savefig(output_file, format='off')

if __name__ == "__main__":

    # Test case 1
    # a, b, c = 4, 6, 8
    # ellipsoid_function = lambda x, y, z : (x**2 / a**2 + y**2 / b**2 + z**2 / c**2) <= 1

    # draw_surface(ellipsoid_function, "ellipsoid_3d.eps", -10, -10, -10, 10, 10, 10)

    # Test case 1
    r = 5
    ellipsoid_function = lambda x, y, z : (x**2 + y**2 + z**2 ) <= r**2

    draw_surface(ellipsoid_function, "sphere_3d.eps", -10, -10, -10, 10, 10, 10)
    
