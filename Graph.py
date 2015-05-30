""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc
from Vectors import Vector2
from Snap import EndPoint, MidPoint, Centre, VerticalInline, HorizontalInline, Horizontal, Vertical
import operator
from math import sqrt

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

    def snap(self, clicks, v, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""
        result = None
        snaps = []
        d2 = d * d  # d is distance squared

        '''Check the two end points'''
        distance = self.v0.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(self.v0, distance))

        distance = self.v1.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(self.v1, distance))

        '''Check the middle point'''
        mid = self.v0.mid(self.v1)
        distance = mid.dist2(v)
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        '''find the nearest marker'''
        snaps.sort(key=operator.attrgetter('distance'))
        if len(snaps) > 0:
            result = snaps[0]
        else:
            '''Check for line ups'''
            d = sqrt(d)
            if abs(self.v0.x - v.x) < d:
                v.x = self.v0.x
                snaps.append(VerticalInline(v, self.v0, d))
            if abs(self.v0.y - v.y) < d:
                v.y = self.v0.y
                snaps.append(HorizontalInline(v, self.v0, d))
            if abs(self.v1.x - v.x) < d:
                v.x = self.v1.x
                snaps.append(VerticalInline(v, self.v1, d))
            if abs(self.v1.y - v.y) < d:
                v.y = self.v1.y
                snaps.append(HorizontalInline(v, self.v1, d))

            if len(snaps) > 0:
                snaps.sort(key=operator.attrgetter('distance'))
                result = snaps[0]
            else:
                '''More Snaps - vertical and horizontal'''
                if len(clicks) > 0:  # if not first click
                    if abs(self.v0.x - v.x) < 10:  # Near vertical
                        v.x = self.v0.x
                        result = Vertical(self.v0, v, distance)
                    if abs(self.v0.y - v.y) < 10:  # Near horizontal
                        v.y = self.v0.y
                        result = Horizontal(self.v0, v, distance)
                    # TODO: Could add Square snap here to snap to 45 degree increments

        return result  # If there is one


class Circle(Graph):
    """ Concrete class for graphics circles"""

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def snap(self, clicks, v, d):
        result = None
        centre = self.v0.mid(self.v1)
        d2 = d * d
        distance = centre.dist2(v)
        if distance < d2:
            result = Centre(centre, distance)
        return result  # If there is one


class Rectangle(Graph):
    """ Concrete class for rectangles"""

    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1

    def snap(self, clicks, v, d):
        result = None
        snaps = []
        d2 = d * d  # Squares are quicker than sqrt
        '''Check the four corners for endpoints'''
        distance = self.v0.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(self.v0, distance))

        va = Vector2(self.v1.x, self.v0.y)
        distance = va.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(va, distance))

        distance = self.v1.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(self.v1, distance))

        vb = Vector2(self.v0.x, self.v1.y)
        distance = vb.dist2(v)
        if distance < d2:
            snaps.append(EndPoint(vb, distance))

        '''Check the four mid points'''
        mid = self.v0.mid(va)
        distance = mid.dist2(v)
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = va.mid(self.v1)
        distance = mid.dist2(v)
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = self.v1.mid(vb)
        distance = mid.dist2(v)
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = vb.mid(self.v0)
        distance = mid.dist2(v)
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        '''Check for near Square'''
        """
        '''Commented out due to bug'''
        if len(clicks) > 0:
            width = abs(self.v0.x - v.x)
            height = abs(self.v0.y - v.y)
            distance = abs(width - height)
            if distance < sqrt(d):
                ave = (width + height) / 2
                self.v1 = Vector2(0,0)  # Just to initiate a Vector2 variable
                if self.v0.x < v.x:
                    self.v1.x = self.v0.x + ave
                else:
                    self.v1.x = self.v0.x - ave
                if self.v0.y < v.y:
                    self.v1.y = self.v0.y + ave
                else:
                    self.v1.y = self.v0.y - ave
                snaps.append(Square(self.v0, self.v1, distance))
        """
        '''Find the closest marker'''
        if len(snaps) > 0:
            snaps.sort(key=operator.attrgetter('distance'))
            result = snaps[0]
        return result # If there is one


class Text(Graph):
    """ Concrete class for graphics text
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, v0, text):
        self.v0 = v0
        self.text = text


class Pline(Graph):
    def __init__(self, nodes, close):
        self.nodes = nodes
        self.close = close

    def snap(self, clicks, v, d):
        result = None
        snaps = []
        d2 = d*d
        for node in self.nodes:  # Run through every node for an end point match
            distance = v.dist2(node)
            if distance < d2:
                snaps.append(EndPoint(node, distance))
        for i in range(0,len(self.nodes)-1):  # Run through every line for a mid point match
            mid = self.nodes[i].mid(self.nodes[i+1])
            distance = v.dist2(mid)
            if distance < d2:
                snaps.append(MidPoint(mid, distance))
        if self.close:
            mid = self.nodes[0].mid(self.nodes[-1])  # Check mid point between first and last nodes
            distance = v.dist2(mid)
            if distance < d2:
                snaps.append(MidPoint(mid, distance))

        '''Find the closest marker'''
        if len(snaps) > 0:
            snaps.sort(key=operator.attrgetter('distance'))
            result = snaps[0]
        return result # If there is one

class Group(Graph):
    """ Concrete class for graphics group
    Implements the composite pattern
    All drawing data is contained within a single group called main.
    """

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, graph):
        self.children.append(graph)

    def snap(self, clicks, v, d):
        result = None
        snaps = []
        '''Go through each graphics object looking for snaps'''
        for child in self.children:
            snap = child.snap(clicks,v, d)
            if snap:  # if there is a find
                snaps.append(snap)
        '''Find the closest snaps'''
        if len(snaps) > 0:
            snaps.sort(key=operator.attrgetter('distance'))
            result = snaps[0]
        return result
