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

    def dist2(self, v):
        """Returns distance squared between self and v.
        Note: This is faster than completing a full square root"""
        dx = self.x - v.x
        dy = self.y - v.y
        return dx*dx + dy*dy

    def distance(self, v):
        """The true distance between self and v.
        Unlike dist2 this does use sqrt and does return the true distance"""
        return sqrt(self.dist2(v))

    def mid(self, v):
        mx = int(self.x + (v.x - self.x)/2)
        my = int(self.y + (v.y - self.y)/2)
        return Vector2(mx, my)

    def near(self, v, d):
        """True if v is within distance d of self"""
        d2 = d*d
        if self.dist(v) < d2:
            result = True
        else:
            result = False
        return result