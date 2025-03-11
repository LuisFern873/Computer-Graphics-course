import matplotlib.pyplot as plt
import numpy as np

# By: Luis Méndez 

# p3 ---- p4
# |        |
# |        |
# p1 ---- p2

def parse_json_to_lambda(json_data):
    op = json_data["op"]
    function = json_data["function"]
    childs = json_data["childs"]
    
    if op == "":
        return lambda x, y: eval(function.replace('^', '**')) <= 0
    
    elif op == "union":
        conditions = [parse_json_to_lambda(child) for child in childs]
        return lambda x, y: np.logical_or.reduce([condition(x, y) for condition in conditions])
    elif op == "intersection":
        conditions = [parse_json_to_lambda(child) for child in childs]
        return lambda x, y: np.logical_and.reduce([condition(x, y) for condition in conditions]) 
    else:
        raise ValueError(f"Unsupported operation '{op}'")

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

def marching_squares(function, output_file, min_x, min_y, max_x, max_y, epsilon):

    x = np.arange(min_x, max_x + 1, epsilon)
    y = np.arange(min_y, max_y + 1, epsilon)
    x, y = np.meshgrid(x, y)

    function = parse_json_to_lambda(function)

    for i in range(0, len(x) - 1):
        for j in range(0, len(y) - 1):
            p1 = (x[i][j], y[i][j])
            p2 = (x[i][j + 1], y[i][j + 1])
            p3 = (x[i + 1][j], y[i + 1][j])
            p4 = (x[i + 1][j + 1], y[i + 1][j + 1])
            evaluate_case(function, p1, p2, p3, p4)

    mask = function(x, y)

    plt.plot(x[mask], y[mask], marker='o', color='r', linestyle='none', markersize=2)
    plt.plot(x[~mask], y[~mask], marker='o', color='k', linestyle='none', markersize=2)
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.grid()
    plt.savefig(output_file, format='eps')
    plt.show()


# Test cases

example_json = {
    "op": "union",
    "function": "",
    "childs": [
        {
            "op": "",
            "function": "(x-2)^2 + (y-3)^2 - 4^2",
            "childs": []
        },
        {
            "op": "",
            "function": "(x+1)^2 + (y-3)^2 - 4^2",
            "childs": []
        },
    ]
}


marching_squares(
    example_json,
    'example-marching-squares-1.eps',
    -5, -5, 6, 6,
    0.1
)

marching_squares(
    # one circle of radius 1 centered at (2, 2)
    {"op":"", "function":"(x-2)^2+(y-2)^2-1", "childs":[]},
    'example-marching-squares-2.eps',
    -5, -5, 6, 6,
    0.1
)

marching_squares(
    {"op":"union", "function":"","childs":[
    # circles of radius 1 centered at (2, 2) and (4, 2)
{"op":"", "function":"(x-2)^2+(y-2)^2-1", "childs":[]},
{"op":"", "function":"(x-4)^2+(y-2)^2-1", "childs":[]}]},
'example-marching-squares-3.eps',
-5, -5, 6, 6,
0.1)



    