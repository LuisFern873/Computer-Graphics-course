from rtree import index
import math
import random
import matplotlib.pyplot as plt

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_closest_points(points):

    # Create an R-tree index
    p = index.Property()
    p.dimension = 2
    idx = index.Index(properties=p)

    # Insert points into the R-tree
    for i, point in enumerate(points):
        idx.insert(i, (point[0], point[1], point[0], point[1]))

    min_distance = float('inf')
    closest_pair = None

    # Find the closest pair of points
    for i, point in enumerate(points):
        nearest = list(idx.nearest((point[0], point[1], point[0], point[1]), 2))

        nearest.remove(i)
        for j in nearest:
            dist = euclidean_distance(point, points[j])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (point, points[j])

    return closest_pair, min_distance


# Example usage with 1000 random points
random.seed(42)
points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(1000)]

closest_pair, distance = find_closest_points(points)

point1, point2 = closest_pair

x_all, y_all = zip(*points)
x_closest, y_closest = zip(*closest_pair)

plt.scatter(x_all, y_all, color='blue', label='Other Points', s=2)
plt.scatter(x_closest, y_closest, color='red', label='Closest Pair', s=2)
plt.legend()
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Random Points with Closest Pair Highlighted')
plt.show()

