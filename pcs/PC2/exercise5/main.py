
# Utilizo un Ray Right para cada punto
# si este choca en una cantidad impar de vertices, esta en el poligono,
# caso contrario no lo esta

def isPointInPolygon(P, A):
    x, y = A
    n = len(P)
    inside = False

    for i in range(n):
        j = (i + 1) % n  # proximo vertice d
        xi, yi = P[i]
        xj, yj = P[j]

        # Comprobar si el punto está en un borde
        if (yi > y) != (yj > y):
            intersect_x = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < intersect_x:
                inside = not inside

    return inside


polygon = [(1, 1), (1, 3), (3, 3), (3, 1)]
point = (2, 2)
print(isPointInPolygon(polygon, point))

point = (4, 2)
print(isPointInPolygon(polygon, point))

