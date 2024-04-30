from math import sqrt

def get_distance(pointA, pointB):
    Ax, Ay, Az = pointA
    Bx, By, Bz = pointB
    return sqrt((Ax-Bx)**2+(Ay-By)**2+(Az-Bz)**2)

def normalize(vector):
    x, y, z = vector
    l = get_distance((0, 0, 0), vector)
    x /= l
    y /= l
    z /= l
    return x, y, z
