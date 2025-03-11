
# Points
# p0 = (x0, y0)
# p1 = (x1, y1) 
# p2 = (x2, y2)

# Vectors
# p0p1 = ( x1 - x0, y1 - y0 )
# p0p2 = ( x2 - x0, y2 - y0 )

# Cross product
# p0p1 x p0p2 = (x1 - x2)(y0 - y2) - (x0 - x2)(y1 - y2)
def cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x2)*(y0 - y2) - (x0 - x2)*(y1 - y2)

# Orientation
def orientation(x0, y0, x1, y1, x2, y2):
    product = cross_product(x0, y0, x1, y1, x2, y2)
    if (product > 0):
        return 0 # clockwise
    elif (product < 0):
        return 1 # counter clockwise
    else:
        return -1 # collinear

# One dimension ...
# Point x0 is on segment [x1, x2]?
# p = min(x1, x2) q = max(x1, x2)
# if p <= x0 y x0 <= q return True

# Now, in two dimensions ...
# Point (x0, y0) is on the segment [(x1, y1) (x2, y2)]?
def is_on_segment(x0, y0, x1, y1, x2, y2):
    return x0 <= max(x1, x2) and x0 >= min(x1, x2) and y0 <= max(y1, y2) and y0 >= min(y1, y2)

def dont_intersect(x0, y0, x1, y1, x2, y2, x3, y3):

    o1 = orientation(x0, y0, x1, y1, x2, y2)
    o2 = orientation(x0, y0, x1, y1, x3, y3)
    o3 = orientation(x2, y2, x3, y3, x0, y0)
    o4 = orientation(x2, y2, x3, y3, x1, y1)

    print(o1, o2, o3, o4)

    if o1 != o2 and o3 != o4:
        return False
    
    # Collinear cases
    if (
        (o1 == -1 and is_on_segment(x2, y2, x0, y0, x1, y1)) or
        (o2 == -1 and is_on_segment(x3, y3, x0, y0, x1, y1)) or
        (o3 == -1 and is_on_segment(x0, y0, x2, y2, x3, y3)) or
        (o4 == -1 and is_on_segment(x1, y1, x2, y2, x3, y3))
    ):
        return False

    return True


result = dont_intersect(1, 6, 3, 4, 5, 2, 2, 5)


print(result)




