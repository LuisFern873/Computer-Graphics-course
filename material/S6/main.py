

class Point:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
class Triangle:
    def __init__(self, p1 : Point, p2 : Point, p3 : Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def __str__(self):
        return f"[{self.p1}, {self.p2}, {self.p3}]"
    
    def area(self):
        x1 = self.p1.x
        x2 = self.p2.x
        x3 = self.p3.x
        y1 = self.p1.y
        y2 = self.p2.y
        y3 = self.p3.y
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

# point (x, y)

# pr lies in the interior of the triangle pi pj pk

def PointIsInTriangle(point : Point, triangle : Triangle):

    A = triangle.area()
    
    return 

pr = Point(0, 1)
print(pr)

triangle = Triangle(Point(0, 1), Point(1, 1), Point(2,2))

print(triangle)

