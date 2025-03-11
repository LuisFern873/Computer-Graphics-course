import matplotlib.pyplot as plt

# Douglas-Peucker
# Based on: https://cartography-playground.gitlab.io/playgrounds/douglas-peucker-algorithm/

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"

def perpendicularDistance(point, start, end):
    if start.x == end.x and start.y == end.y:
        return ((point.x - start.x) ** 2 + (point.y - start.y) ** 2) ** 0.5
    
    num = abs((end.y - start.y) * point.x - (end.x - start.x) * point.y + end.x * start.y - end.y * start.x)
    den = ((end.y - start.y) ** 2 + (end.x - start.x) ** 2) ** 0.5
    return num / den

# C: ORDERED (x-axis) set of points
# epsilon: tolerance

def douglasPeucker(C : list[Point], epsilon : float):
    first, last = C[0], C[-1]
    dmax = 0
    index = 0
    for i in range(1, len(C) - 1):
        d = perpendicularDistance(C[i], first, last)
        if d > dmax:
            index, dmax = i, d
    
    if dmax > epsilon:
        results1 = douglasPeucker(C[:index + 1], epsilon)
        results2 = douglasPeucker(C[index:], epsilon)
        result = results1[:-1] + results2
    else:
        result = [first, last]
    
    return result

def plot_points(original, simplified):
    fig, ax = plt.subplots()
    
    original_x = [p.x for p in original]
    original_y = [p.y for p in original]
    ax.plot(original_x, original_y, 'bo-', label='Original')
    
    simplified_x = [p.x for p in simplified]
    simplified_y = [p.y for p in simplified]
    ax.plot(simplified_x, simplified_y, 'ro-', label='Simplified')
    
    ax.legend()
    ax.set_title('Douglas-Peucker Algorithm')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.show()

if __name__ == "__main__":
    points = [
        Point(0, 0), Point(1, 0.1), Point(2, -0.1), Point(3, 5), Point(4, 6),
        Point(5, 7), Point(6, 8), Point(7, 8.1), Point(8, 8), Point(9, 0)
    ]
    epsilon = 1.0
    simplified_points = douglasPeucker(points, epsilon)
    
    print("Original points:")
    for p in points:
        print(p)
    
    print("\nSimplified points:")
    for p in simplified_points:
        print(p)

    plot_points(points, simplified_points)