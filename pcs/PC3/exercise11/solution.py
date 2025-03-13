import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from skimage import measure

# By: Luis Méndez 

def parse_json_to_lambda(json_data):
    op = json_data["op"]
    function = json_data["function"]
    childs = json_data["childs"]
    
    if op == "":
        return lambda x, y, z: eval(function.replace('^', '**')) <= 0
    
    elif op == "union":
        conditions = [parse_json_to_lambda(child) for child in childs]
        return lambda x, y, z: np.logical_or.reduce([condition(x, y, z) for condition in conditions])
    elif op == "intersection":
        conditions = [parse_json_to_lambda(child) for child in childs]
        return lambda x, y, z: np.logical_and.reduce([condition(x, y, z) for condition in conditions]) 
    else:
        raise ValueError(f"Unsupported operation '{op}'")

def marching_cubes(function, output_file, min_x, min_y, min_z, max_x, max_y, max_z, precision):

    x = np.arange(min_x, max_x + 1, 1)
    y = np.arange(min_y, max_y + 1, 1)
    z = np.arange(min_z, max_z + 1, 1)
    x, y, z = np.meshgrid(x, y, z)

    function = parse_json_to_lambda(function)

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
    plt.savefig(output_file, format='eps')
    plt.show()
  

if __name__ == "__main__":
    
    example_json = {
      "op": "union",
      "function": "",
      "childs": [
        {
          "op": "",
          "function": "(x-2)^2 + (y-3)^2 + (z-3)^2 - 4^2",
          "childs": []
        },
        {
          "op": "",
          "function": "(x+1)^2 + (y-3)^2 + (z-3)^2 - 4^2",
          "childs": []
        }
      ]
    }

    # example_json = lambda x, y, z : np.logical_or.reduce([
    #     (x-2)**2 + (y-3)**2 + (z-3)**2 - 4**2 <= 0, 
    #     (x+1)**2 + (y-3)**2 + (z-3)**2 - 4**2 <= 0
    # ])

    marching_cubes(
        example_json,
        'example-marching-cubes-1.eps',
        -5, -5, -5, 6, 6, 6,
        0.1
    )

    marching_cubes(
    # sphere of radius 1 centered at (2, 2, 2)
    {"op":"", "function":"(x-2)^2+(y-2)^2+(z-2)^2-1", "childs":[]},
    'example-marching-cubes-2.eps',
    -5, -5, -5, 6, 6, 6,
    0.1)

    marching_cubes(
    {"op":"union", "function":"", "childs":[
    {"op":"", "function":"(x-2)^2+(y-2)^2+(z-2)^2-1", "childs":[]},
    {"op":"", "function":"(x-4)^2+(y-2)^2+(z-2)^2-1", "childs":[]}
    ]},
    'example-marching-cubes-3.eps',
    -5, -5, -5, 6, 6, 6,
    0.1)