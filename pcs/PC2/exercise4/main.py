
class Point:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, p1 : Point, p2 : Point, p3 : Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def area(self):
        return abs(
            self.p1.x * self.p2.y +
            self.p2.x * self.p3.y +
            self.p3.x * self.p1.y -
            self.p1.x * self.p3.y -
            self.p2.x * self.p1.y -
            self.p3.x * self.p2.y
        ) / 2.0


def is_in_triangle(p : Point, triangle : Triangle):

    A = triangle.area()

    T1 = Triangle(p, triangle.p1, triangle.p2)
    A1 = T1.area()

    T2 = Triangle(triangle.p1, p, triangle.p3)
    A2 = T2.area()

    T3 = Triangle(triangle.p2, triangle.p3, p)
    A3 = T3.area()

    return A == (A1 + A2 + A3)

triangle = Triangle(Point(-3, -2), Point(3, 5), Point(6, -4))
p = Point(2, 0)

result = is_in_triangle(p, triangle)

print(result)