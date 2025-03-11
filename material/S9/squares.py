import matplotlib.pyplot as plt
import numpy as np

# By: Luis Méndez 

# p3 ---- p4
# |        |
# |        |
# p1 ---- p2

def midpoint(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

def evaluate_case(function, p1, p2, p3, p4):
    isovalues = (
        function(p1[0], p1[1]), 
        function(p2[0], p2[1]), 
        function(p3[0], p3[1]), 
        function(p4[0], p4[1])
    )
    match isovalues:
        case (1, 0, 0, 0) | (0, 1, 1, 1): # case 1 y 14
            plt.plot(*zip(midpoint(p1, p2), midpoint(p1, p3)), color='r')
        case (0, 1, 0, 0) | (1, 0, 1, 1): # case 2 y 13
            plt.plot(*zip(midpoint(p1, p2), midpoint(p2, p4)), color='r')
        case (1, 1, 0, 0) | (0, 0, 1, 1): # case 3 y 12
            plt.plot(*zip(midpoint(p1, p3), midpoint(p2, p4)), color='r')
        case (0, 0, 0, 1) | (1, 1, 1, 0):
            plt.plot(*zip(midpoint(p3, p4), midpoint(p2, p4)), color='r')
        case (1, 0, 0, 1): # case 5
            plt.plot(*zip(midpoint(p1, p3), midpoint(p3, p4)), color='r')
            plt.plot(*zip(midpoint(p1, p2), midpoint(p2, p4)), color='r')
        case (0, 1, 0, 1) | (1, 0, 1, 0): # case 6 y 9
            plt.plot(*zip(midpoint(p1, p2), midpoint(p3, p4)), color='r')
        case (1, 1, 0, 1) | (0, 0, 1, 0): # case 7 y 8
            plt.plot(*zip(midpoint(p1, p3), midpoint(p3, p4)), color='r')
        case (0, 1, 1, 0): # case 10
            plt.plot(*zip(midpoint(p1, p2), midpoint(p1, p3)), color='r')
            plt.plot(*zip(midpoint(p3, p4), midpoint(p2, p4)), color='r')

def draw_curve(function, output_file, min_x, min_y, max_x, max_y, epsilon):

    x = np.arange(min_x, max_x + 1, epsilon)
    y = np.arange(min_y, max_y + 1, epsilon)
    x, y = np.meshgrid(x, y)

    for i in range(0, len(x) - 1):
        for j in range(0, len(y) - 1):
            p1 = (x[i][j], y[i][j])
            p2 = (x[i][j + 1], y[i][j + 1])
            p3 = (x[i + 1][j], y[i + 1][j])
            p4 = (x[i + 1][j + 1], y[i + 1][j + 1])
            evaluate_case(function, p1, p2, p3, p4)

    plt.plot(x[function(x, y)], y[function(x, y)], marker='o', color='r', linestyle='none', markersize=2)
    plt.plot(x[~function(x, y)], y[~function(x, y)], marker='o', color='k', linestyle='none', markersize=2)
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.grid()
    plt.show()
    plt.savefig(output_file, format='eps')

if __name__ == "__main__":

    # Test case 1
    some_function = lambda x, y : 0.004 + 0.110 * x - 0.177 * y - 0.174 * x**(2) + 0.224 * x * y -0.303 * y**(2) - 0.168 * x**(3) + 0.327 * x**(2) * y - 0.087 * x * y**(2) - 0.013 *y**(3) + 0.235 * x**(4) - 0.667 * x**(3) * y + 0.745 * x**(2) * y**(2) - 0.029 * x * y**(3)+ 0.072 * y**(4) <= 0
    draw_curve(some_function, "some.eps", -5, -5, 5, 5, 0.2)

    # Test case 2
    a = 4
    b = 9
    ellipse_function = lambda x, y : (x**2 / a**2 + y**2 / b**2) <= 1
    draw_curve(ellipse_function, "ellipse.eps", -10, -10, 10, 10, 0.4)



    