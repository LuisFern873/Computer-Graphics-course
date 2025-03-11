

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def orientation(p : Point, q : Point, r : Point):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0: 
        return 0 # collinear
    elif val > 0:
        return 1 # clockwise
    else:
        return 2 # counterclockwise
    
def inSegment(a : Point, b : Point, p : Point):
    return (
        min(a.x, b.x) <= p.x and 
        p.x <= max(a.x, b.x) and 
        min(a.y, b.y) <= p.y and 
        p.y <= max(a.y, b.y)
    ) and orientation(a, p, b) == 0

a = Point(-1, -1)
b = Point(2, 2)
p = Point(0.5, 0.5)

print(inSegment(a, b, p))