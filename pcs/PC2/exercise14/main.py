import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"

def triangleArea(p1, p2, p3):
    return 0.5 * abs(p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))

def visvalingamWhyatt(points, threshold):

    if len(points) < 3:
        return points

    areas = [triangleArea(points[i - 1], points[i], points[i + 1]) for i in range(1, len(points) - 1)]
    areas = [float('inf')] + areas + [float('inf')]

    while True:
        min_area = min(areas)
        if min_area >= threshold:
            break
        
        index = areas.index(min_area)
        points.pop(index)
        areas.pop(index)

        if index > 1:
            areas[index - 1] = triangleArea(points[index - 2], points[index - 1], points[index])
        if index < len(points) - 1:
            areas[index] = triangleArea(points[index - 1], points[index], points[index + 1])
        
    return points

def plot_points(original, simplified):
    fig, ax = plt.subplots()

    original_x = [p.x for p in original]
    original_y = [p.y for p in original]
    ax.plot(original_x, original_y, 'bo-', label='Original')

    simplified_x = [p.x for p in simplified]
    simplified_y = [p.y for p in simplified]
    ax.plot(simplified_x, simplified_y, 'ro-', label='Simplified')
    
    ax.legend()
    ax.set_title('Visvalingam-Whyatt Algorithm')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.show()
    
if __name__ == "__main__":
    points = [
        Point(0, 0), Point(1, 0.1), Point(2, -0.1), Point(3, 5), Point(4, 6),
        Point(5, 7), Point(6, 8), Point(7, 8.1), Point(8, 8), Point(9, 0)
    ]
    threshold = 1.0
    simplified_points = visvalingamWhyatt(points.copy(), threshold)
    
    print("Original points:")
    for p in points:
        print(p)
    
    print("\nSimplified points:")
    for p in simplified_points:
        print(p)
    
    plot_points(points, simplified_points)
