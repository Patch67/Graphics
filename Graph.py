""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc
from Vectors import Vector2, Vector2Pair


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

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def snap(self, v, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""

        d2 = d * d  # d is distance squared

        '''Check the two end points'''
        if Vector2Pair(self.v0, v).dist2() < d2:
            return ["End", self.v0]  # return coordinates of start point
        if Vector2Pair(self.v1, v).dist2() < d2:
            return ["End", self.v1]  # return coordinates of end point

        '''Check the middle point'''
        mid = Vector2Pair(self.v0, self.v1).mid()
        if Vector2Pair(mid, v).dist2() < d2:
            return ["Mid", mid]  # return coordinates of middle point

        '''Check for line ups'''
        if abs(self.v0.x - v.x) < d:
            v.x = self.v0.x
            return ["Inline", v, self.v0]
        if abs(self.v0.y - v.y) < d:
            v.y = self.v0.y
            return ["Inline", v, self.v0]
        if abs(self.v1.x - v.x) < d:
            v.x = self.v1.x
            return ["Inline", v, self.v1]
        if abs(self.v1.y - v.y) < d:
            v.y = self.v1.y
            return ["Inline", v, self.v1]

        return None  # No matches found


class Circle(Graph):
    """ Concrete class for graphics circles"""

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def snap(self, v, d):
        centre = Vector2Pair(self.v0, self.v1).mid()
        d2 = d * d
        if Vector2Pair(centre, v).dist2() < d2:
            return ["Centre", centre]
        else:
            return None


class Rectangle(Graph):
    """ Concrete class for rectangles"""

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def snap(self, v, d):
        d2 = d * d  # Squares are quicker than sqrt
        '''Check the four corners'''
        if Vector2Pair(self.v0, v).dist2() < d2:
            return ["End", self.v0]
        va = Vector2(self.v1.x, self.v0.y)
        if Vector2Pair(va, v).dist2() < d2:
            return ["End", va]
        if Vector2Pair(self.v1, v).dist2() < d2:
            return ["End", self.v1]
        vb = Vector2(self.v0.x, self.v1.y)
        if Vector2Pair(vb, v).dist2() < d2:
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

    def __init__(self, v0, text):
        self.v0 = v0
        self.text = text

    def snap(self, v, d):
        # TODO: Add code for Text pick
        return None


class Pline(Graph):
    def __init__(self, nodes, close):
        self.nodes = nodes
        self.close = close

    def snap(self, v, d):
        d2 = d*d
        for node in self.nodes:  # Run through every node for an end point match
            if Vector2Pair(v, node).dist2() < d2:
                return ["End", node]  # If the snap result is a class then we won't have to do loads of if's later
        for i in range(0,len(self.nodes)-1):  # Run through every line for an mid point match
            mid = Vector2Pair(self.nodes[i], self.nodes[i+1]).mid()
            if Vector2Pair(v, mid).dist2() < d2:
                return ["Mid", mid]
        if self.close:
            mid = Vector2Pair(self.nodes[0], self.nodes[-1]).mid()  # Check mid point between first and last nodes
            if Vector2Pair(v, mid).dist2() < d2:
                return ["Mid", mid]

class Group(Graph):
    """ Concrete class for graphics group
    Implements the composite pattern
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, graph):
        self.children.append(graph)

    def snap(self, v, d):
        for child in self.children:
            marker = child.snap(v, d)
            if marker:  # if there is a find
                return marker  # return a the coordinates
        return None  # if no finds then return None
