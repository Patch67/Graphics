""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc
from Vectors import Vector2, Vector2Pair
from Snap import Snap, EndPoint, MidPoint, Centre, VerticalInline, HorizontalInline, Horizontal, Vertical, Square
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
        # TODO: All snaps should be done in overrides of this and the best result returned.
        '''
         Instead of just passing in the current mouse press we should also pass in the previous
         so we can check for horizontal and vertical alignment too.
         In the case of poly line we could check for end and mid point snaps on the construction lines too.
        '''
        pass

    def get_endpoint(self, v, d):
        result = None
        snaps = []
        d2 = d*d
        distance = Vector2Pair(self.v0, v).dist2()
        if distance < d2:
            snaps.append(Snap(self.v0, distance))

        distance = Vector2Pair(self.v1, v).dist2()
        if distance < d2:
            snaps.append(Snap(self.v1, distance))

        snaps.sort()
        if len(snaps) > 0:
            result = snaps[0]
        return result


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
        distance = Vector2Pair(self.v0, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(self.v0, distance))
        distance = Vector2Pair(self.v1, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(self.v1, distance))

        '''Check the middle point'''
        mid = Vector2Pair(self.v0, self.v1).mid()
        distance = Vector2Pair(mid, v).dist2()
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        '''find the nearest marker'''
        snaps.sort()
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

            snaps.sort(key=operator.attrgetter('distance'))
            if len(snaps) > 0:
                result = snaps[0]
            else:
                '''More Snaps - previously in temp.snap'''
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
        centre = Vector2Pair(self.v0, self.v1).mid()
        d2 = d * d
        distance = Vector2Pair(centre, v).dist2()
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
        distance = Vector2Pair(self.v0, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(self.v0, distance))

        va = Vector2(self.v1.x, self.v0.y)
        distance = Vector2Pair(va, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(va, distance))

        distance = Vector2Pair(self.v1, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(self.v1, distance))

        vb = Vector2(self.v0.x, self.v1.y)
        distance = Vector2Pair(vb, v).dist2()
        if distance < d2:
            snaps.append(EndPoint(vb, distance))



        '''Check the four mid points'''
        mid = Vector2Pair(self.v0, va).mid()
        distance = Vector2Pair(mid, v).dist2()
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = Vector2Pair(va, self.v1).mid()
        distance = Vector2Pair(mid, v).dist2()
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = Vector2Pair(self.v1, vb).mid()
        distance = Vector2Pair(mid, v).dist2()
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        mid = Vector2Pair(vb, self.v0).mid()
        distance = Vector2Pair(mid, v).dist2()
        if distance < d2:
            snaps.append(MidPoint(mid, distance))

        '''Check for near Square'''
        if len(clicks) > 0:
            width = abs(self.v0.x - v.x)
            height = abs(self.v0.y - v.y)
            distance = abs(width - height)
            if distance < 10:
                ave = (width + height) / 2
                self.v1 = v  # Just to initiate a Vector2 variable
                if self.v0.x < v.x:
                    self.v1.x = self.v0.x + ave
                else:
                    self.v1.x = self.v0.x - ave
                if self.v0.y < v.y:
                    self.v1.y = self.v0.y + ave
                else:
                    self.v1.y = self.v0.y - ave
                snaps.append(Square(self.v0, self.v1, distance))

        '''Find the closest marker'''
        snaps.sort(key=operator.attrgetter('distance'))
        if len(snaps) > 0:
            result = snaps[0]
        return result # If there is one


class Text(Graph):
    """ Concrete class for graphics text
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, v0, text):
        self.v0 = v0
        self.text = text

    def snap(self, clicks, v, d):
        # TODO: Add code for Text pick
        return None


class Pline(Graph):
    def __init__(self, nodes, close):
        self.nodes = nodes
        self.close = close

    def snap(self, clicks, v, d):
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
    All drawing data is contained within a single group called main.
    """

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, graph):
        self.children.append(graph)

    def snap(self, clicks, v, d):
        snaps = []
        '''Go through each graphics object looking for snaps'''
        for child in self.children:
            snap = child.snap(clicks,v, d)
            if snap:  # if there is a find
                snaps.append(snap)
        '''Find the closest snaps'''
        snaps.sort(key=operator.attrgetter('distance'))
        if len(snaps) > 0:
            result = snaps[0]
        else:
            result = None
        return result
