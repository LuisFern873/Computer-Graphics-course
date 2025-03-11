import numpy as np

def distance_point_to_line(P, Q, d):

    PQ = np.array([P[0] - Q[0], P[1] - Q[1], P[2] - Q[2]])

    cross_product = np.cross(d, PQ)
    
    cross_product_magnitude = np.linalg.norm(cross_product)

    d_magnitude = np.linalg.norm(d)
    
    distance = cross_product_magnitude / d_magnitude
    
    return distance

P = (1, 2, 3)
Q = (4, 5, 6)
d = (1, 0, 0)

distance = distance_point_to_line(P, Q, d)
print("Distance from point to line:", distance)
