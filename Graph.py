""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc
from Vectors import Vector2
from Snap import EndPoint, MidPoint, Centre, VerticalInline, HorizontalInline, Horizontal, Vertical, Square
import operator
#from math import sqrt # POSTPONED UNTIL VERSION 0.2

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

    def in_bounding_box(self, v):
        """Returns true if v is inside the bounding box"""
        lo = Vector2(min(self.v0.x, self.v1.x), min(self.v0.y, self.v1.y))
        hi = Vector2(max(self.v0.y, self.v1.x), max(self.v0.x, self.v1.y))
        return v.x >= lo.x and v.x <= hi.x and v.y >= lo.y and v.y <= hi.y

    @abc.abstractmethod
    def pick(self, v, d):
        """Returns true if v is within d units of object"""
        result = False
        if self.in_bounding_box(v):
            pass
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
            """TODO: Thee could be a situation where a mouse is near to a horizontal and a vertical inline.
            This might mean making a DualInline marker or it could mean returning multiple snaps instead of just one
            """
            """POSTPONED UNTIL VERSION 0.2
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
            """
            if len(snaps) > 0:
                snaps.sort(key=operator.attrgetter('distance'))
                result = snaps[0]
        return result  # If there is one

    def pick(self, v, d):
        pass


class Circle:
    """True circle, added in v0.2 to differentiate with oval"""

    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def snap(self, clicks, v, d):
        result = None
        '''Check for centre point'''
        d2 = d * d
        distance = self.centre.dist2(v)
        if distance < d2:
            result = Centre(self.centre, distance)
        else:
            '''Check for quadrants - N, E, S & W'''
            N = Vector2(self.centre.x, self.centre.y + self.radius)
            E = Vector2(self.centre.x + self.radius, self.centre.y)
            S = Vector2(self.centre.x, self.centre.y - self.radius)
            W = Vector2(self.centre.x - self.radius, self.centre.y)
            distance = N.dist2(v)
            if distance < d2:
                result = MidPoint(N, distance)
            else:
                distance = E.dist2(v)
                if distance < d2:
                    result = MidPoint(E, distance)
                else:
                    distance = S.dist2(v)
                    if distance < d2:
                        result = MidPoint(S, distance)
                    else:
                        distance = W.dist2(v)
                        if distance < d2:
                            result = MidPoint(W, distance)
        return result  # If there is one

    def pick(self, v, d):
        result = False
        '''Look for circumference pick'''
        centre = self.v0.mid(self.v1)
        north = Vector2(centre.x, self.v0.y)
        radius = centre.distance(north)
        if abs(centre.distance(v) - radius) < d:
            result = True
        return result


class Oval(Graph):
    """ Concrete class for graphics ovals"""

    def __init__(self, v0, v1):
        self.v0 = Vector2(min(v0.x, v1.x), min(v0.y, v1.y))  # Make v0 the smallest corner
        self.v1 = Vector2(max(v0.x, v1.x), max(v0.y, v1.y))  # Make v1 the largest corner

    def snap(self, clicks, v, d):
        result = None
        '''Check for centre point'''
        centre = self.v0.mid(self.v1)
        d2 = d * d
        distance = centre.dist2(v)
        if distance < d2:
            result = Centre(centre, distance)
        else:
            '''Check for quadrants - N, E, S & W'''
            NW = self.v0
            SE = self.v1
            NE = Vector2(SE.x, NW.y)
            SW = Vector2(NW.x, SE.y)
            N = NW.mid(NE)
            E = NE.mid(SE)
            S = SE.mid(SW)
            W = SW.mid(NW)
            distance = N.dist2(v)
            if distance < d2:
                result = MidPoint(N, distance)
            else:
                distance = E.dist2(v)
                if distance < d2:
                    result = MidPoint(E, distance)
                else:
                    distance = S.dist2(v)
                    if distance < d2:
                        result = MidPoint(S, distance)
                    else:
                        distance = W.dist2(v)
                        if distance < d2:
                            result = MidPoint(W, distance)
        return result  # If there is one

    def in_bounding_box(self, v):
        """Is v inside the bounding box"""
        result = False
        lo = self.v0
        hi = self.v1
        if v.x >= lo.x and v.x <= hi.x and v.y >= lo.y and v.y <= hi.y:
            result = True
        return result

    def is_inside_box(self, lo, hi):
        """Returns true if object is within the given box"""
        result = False
        if lo.x < self.v0.x and lo.y < self.v0.y and hi.x > self.v1.x and hi.y > self.v1.y:
            result = True
        return result

class Rectangle(Graph):
    """ Concrete class for rectangles"""

    def __init__(self, v0, v1):
        self.v0 = Vector2(min(v0.x, v1.x), min(v0.y, v1.y))  # Make v0 the smallest corner
        self.v1 = Vector2(max(v0.x, v1.x), max(v0.y, v1.y))  # Make v1 the largest corner

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

        '''Find the closest marker'''
        if len(snaps) > 0:
            snaps.sort(key=operator.attrgetter('distance'))
            result = snaps[0]
        return result # If there is one

    def pick(self, v, d):
        """This only works if rectangle is not rotated"""
        result = False
        if abs(self.v0.x - v.x) < d and v.y >= self.v0.y and v.y <= self.v1.y:  # Near left edge
            result = True
        elif abs(self.v1.x - v.x) < d and v.y >= self.v0.y and v.y <= self.v1.y:  # Near right edge
            result = True
        elif abs(self.v0.y - v.y) < d and v.x >= self.v0.x and v.x <= self.v1.x:  # Near top edge
            result = True
        elif abs(self.v1.y - v.y) < d and v.x >= self.v0.x and v.x <= self.v1.x:  # Near bottom edge
            result = True
        return result

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
        """TODO:  There could be a situation with inline snaps where multiple matches are made,
        i.e. with a horizontal snap from one object and a vertical snap from another.
        At present the code does not allow for this.
        Perhaps inline matches should be treated differently from simple one point snaps, perhaps they should be object guides"""
        if len(snaps) > 0:
            snaps.sort(key=operator.attrgetter('distance'))
            result = snaps[0]
        return result

    def pick(self, v, d):
        pick_list = []
        for child in self.children:
            if child.pick(v, d):
                pick_list.append(child)
        return pick_list
