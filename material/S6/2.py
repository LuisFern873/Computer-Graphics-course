import math

class Point:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, p1 : Point, p2 : Point):
        self.p1 = p1
        self.p2 = p2
    
    def length(self):
        return math.sqrt((self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2)


def dotProduct(s1 : Segment, s2 : Segment):
    return (s1.p1.x * s2.p1.x + s1.p1.y * s2.p1.y) + (s1.p2.x * s2.p2.x + s1.p2.y * s2.p2.y)

# A·B = |A||B|cos(θ)

p1 = Point(1, 5)
p2 = Point(4, 1)
p3 = Point(6, 6)

A = Segment(p1, p2)
B = Segment(p1, p3)

print(dotProduct(A, B))

print(math.acos(dotProduct(A, B) / (A.length() * B.length())))

# x1
# (x1 * x3 + y1 * y3) + (x2 * x4 + y2 * y4)

# A·B = [(x1, y1), (x2, y2)] · [(x3, y3), (x4, y4)]

