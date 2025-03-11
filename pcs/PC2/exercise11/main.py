import numpy as np

# Based on https://mathworld.wolfram.com/PolygonArea.html

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

def polygonArea(points : list[Point]):
    n = len(points)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n  # Next vertex index
        area += points[i].x * points[j].y
        area -= points[i].y * points[j].x
    
    area = abs(area) / 2.0
    return area

if __name__ == "__main__":
    points = [
        Point(8, 2), Point(10, 4), Point(5, 9), Point(-1, 5), Point(3, 1)
    ]

    area = polygonArea(points)
    print(area)