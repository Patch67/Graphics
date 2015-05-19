""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc


def dist2(x0, y0, x1, y1):
    """Finds the distance squared between two points"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    return dx*dx + dy*dy


def mid(x0, y0, x1, y1):
    """Finds the mid point between two points"""
    mx = int(x0 + (x1 - x0) / 2)  # middle x
    my = int(y0 + (y1 - y0) / 2)  # middle y
    return [mx, my]


class Graph:
    """ Abstract base class from which all graphics object derive"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def snap(self, x, y, d):
        pass


class Line(Graph):
    """ Concrete class for graphics lines"""
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def snap(self, x, y, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""
        d = d*d  # d is distance squared
        '''Check the two end points'''
        if dist2(self.x0, self.y0, x, y) < d:  # if distance <5. Note use of 25 which is 5 squared
            return [self.x0, self.y0]  # return coordinates of start point
        if dist2(self.x1, self.y1, x, y) < d:
            return [self.x1, self.y1]  # return coordinates of end point

        '''Check the middle point'''
        mxy = mid(self.x0, self.y0, self.x1, self.y1)
        if dist2(mxy[0], mxy[1], x, y) < d:
            return mxy  # return coordinates of middle point

        return None  # No matches found


class Circle(Graph):
    """ Concrete class for graphics circles"""
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def snap(self, x, y, d):
        # TODO: Add code for Circle pick
        return None


class Rectangle(Graph):
    """ Concrete class for rectangles"""
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def snap(self, x, y, d):
        d2 = d*d  # Squares are quicker than sqrt
        '''Check the four corners'''
        if dist2(self.x0, self.y0, x, y) < d2:
            return [self.x0, self.y0]
        if dist2(self.x1, self.y0, x, y) < d2:
            return [self.x1, self.y0]
        if dist2(self.x1, self.y1, x, y) < d2:
            return [self.x1, self.y1]
        if dist2(self.x0, self.y1, x, y) < d2:
            return [self.x0, self.y1]

        '''Check the four mid points'''
        mxy = mid(self.x0, self.y0, self.x1, self.y0)
        if dist2(mxy[0], mxy[1], x, y) < d2:
            return mxy  # return coordinates of middle point
        mxy = mid(self.x1, self.y0, self.x1, self.y1)
        if dist2(mxy[0], mxy[1], x, y) < d2:
            return mxy  # return coordinates of middle point
        mxy = mid(self.x1, self.y1, self.x0, self.y1)
        if dist2(mxy[0], mxy[1], x, y) < d2:
            return mxy  # return coordinates of middle point
        mxy = mid(self.x0, self.y1, self.x0, self.y0)
        if dist2(mxy[0], mxy[1], x, y) < d2:
            return mxy  # return coordinates of middle point
        return None


class Text(Graph):
    """ Concrete class for graphics text
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def snap(self, x, y, d):
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

    def snap(self, x, y, d):
        for child in self.children:
            r = child.snap(x, y, d)
            if r:  # if there is a find
                return r  # return a the coordinates
        return None  # if no finds then return None

