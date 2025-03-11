import math

def angle(x0, y0, x1, y1, x2, y2):
    x1 = x1 - x0
    x2 = x2 - x0
    y1 = y1 - y0
    y2 = y2 - y0
    dot = x1*x2 + y1*y2      
    det = x1*y2 - y1*x2     
    return math.atan2(det, dot)

# Si angle es negativo, entonces es > 180
# angle(ps[i][0], ps[i][1], ps[i+1][0], ps[i+1][1], ps[i-1][0], ps[i-1][1])


# Iteramos sobre todos los vertices del poligono
def isConvex(ps):
    n = len(ps)
    for i in range(n):
        an = angle(ps[i][0], ps[i][1], ps[(i+1)%n][0], ps[(i+1)%n][1], ps[i-1][0], ps[i-1][1])
        if an < 0:
            return False
    return True

points = [(1, 3), (3, 1), (6, 2), (5, 5), (2, 6)]

print(isConvex(points))

points = [(1, 3), (3, 1), (6, 2), (5, 5), (4, 3)]

print(isConvex(points))