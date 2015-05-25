__author__ = 'Patrick'
from math import sqrt, atan  # Only needed because of Vector2


class Vector2:
    """Class of 2 Dimensional Vectors and associated methods"""
    def __init__(self, x, y):
        self.x, self.y = x, y;

    def magnitude(self):
        """Returns the size of the vector"""
        return sqrt(self.x*self.x + self.y*self.y)

    def unit(self):
        """Returns a Vector2 of the same direction but only unit length"""
        m = self.magnitude()
        return Vector2(self.x / m, self.y / m)

    def angle(self):
        """Returns anti-clockwise angle between vector and the x axis, in radians"""
        return atan(self.x / self.y)


class Vector2Pair:
    """Class for operations on pairs of 2 dimensional vectors"""
    # TODO: Eliminate this class.  They should be part of Vector2 with a vector as parameter
    def __init__(self, v0, v1):
        self.v0, self.v1 = v0, v1

    def dist2(self):
        """Finds the distance squared between two points.
        It is faster to compare squared numbers than to computer square root"""
        dx = abs(self.v1.x - self.v0.x)
        dy = abs(self.v1.y - self.v0.y)
        return dx*dx + dy*dy

    def mid(self):
        """Finds the mid point between two points"""
        mx = int(self.v0.x + (self.v1.x - self.v0.x) / 2)  # middle x
        my = int(self.v0.y + (self.v1.y - self.v0.y) / 2)  # middle y
        return Vector2(mx, my)


