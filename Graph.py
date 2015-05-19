""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc

class Vector2():
    def __init__(self, x,y):
        self.x, self.y = x, y;

class Vector2Pair():
    def __init__(self, v0, v1):
        self.v0, self.v1 = v0, v1

    def dist2(self):
        """Finds the distance squared between two points.
        It is faster to comapre squared numbers than to computer square root"""
        dx = abs(self.v1.x - self.v0.x)
        dy = abs(self.v1.y - self.v0.y)
        return dx*dx + dy*dy

    def mid(self):
        """Finds the mid point between two points"""
        mx = int(self.v0.x + (self.v1.x - (self.v0.x) / 2)  # middle x
        my = int(self.v0.y + (self.v1.y - self.v0.y) / 2)  # middle y
        return Vector2(mx, my)


class Graph:
    """ Abstract base class from which all graphics object derive"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def snap(self, v, d):
        """Search for coordinates within d - distance or v - Vector, i.e. Mouse click"""
        pass


class Line(Graph):
    """ Concrete class for graphics lines"""
    def __init__(self, x0, y0, x1, y1):
        self.v0 = Vector2(x0,y0)
        self.v1 = Vector2(x1,y1)

    def snap(self, v, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""

        d *= d  # d is distance squared

        '''Check the two end points'''
        if Vector2Pair(self.v0, v).dis2() < d:  # if distance <5. Note use of 25 which is 5 squared
            return ["End", self.v0]  # return coordinates of start point
        if Vector2Pair(self.v1, v).dis2() < d:
            return ["End", self.v1]  # return coordinates of end point

        '''Check the middle point'''
        mid = Vector2Pair(self.v0, self.v1).mid()
        if Vector2Pair(mid, v) < d:
            return ["Mid", mid]  # return coordinates of middle point

        return None  # No matches found


class Circle(Graph):
    """ Concrete class for graphics circles"""
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def snap(self, v, d):
        # TODO: Add code for Circle pick
        return None


class Rectangle(Graph):
    """ Concrete class for rectangles"""
    def __init__(self, x0, y0, x1, y1):
        self.v0 = Vector2(x0, y0)
        self.v1 = Vector2(x1, y1)

    def snap(self, v, d):
        d2 = d*d  # Squares are quicker than sqrt
        '''Check the four corners'''
        if Vector2Pair(self.v0, v).dist2() < d2:
            return ["End", self.v0]
        va = Vector2(self.v1.x, self.v0.y)
        if Vector2Pair(va, v).dist2 < d2:
            return ["End", va]
        if Vector2Pair(self.v1, v).dist2 < d2:
            return ["End", self.v]
        vb = Vector2(self.x0, self.y1)
        if Vector2Pair(vb, v).dist2 < d2:
            return ["End", vb]

        '''Check the four mid points'''
        mid = Vector2Pair(self.v0, va).mid()
        if Vector2Pair(mid, v).dist2() < d2:
            return ["Mid", mid]  # return coordinates of middle point
        mid = Vector2Pair(va, self.v1).mid()
        if Vector2Pair(mid, v).dist2() < d2:
            return ["Mid", mid]  # return coordinates of middle point
        mid = Vector2Pair(self.v1, vb).mid()
        if Vector2Pair(mid, v).dist2() < d2:
            return ["Mid", mid]  # return coordinates of middle point
        mid = Vector2Pair(vb, self.v0).mid()
        if Vector2Pair(mid, v).dist2() < d2:
            return ["Mid", mid]  # return coordinates of middle point

        return None


class Text(Graph):
    """ Concrete class for graphics text
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def snap(self, v, d):
        # TODO: Add code for Text pick
        return None


class Group(Graph):
    """ Concrete class for graphics group
    Implements the composite pattern
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self,name):
        self.name = name
        self.children=[]

    def add(self,graph):
        self.children.append(graph)

    def snap(self, v, d):
        for child in self.children:
            r = child.snap(v, d)
            if r:  # if there is a find
                return r  # return a the coordinates
        return None  # if no finds then return None

