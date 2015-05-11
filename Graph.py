""" Contains Graphics classes based on Compound design pattern

This is a model component of the MVC application design.
As such it houses all the data related classes for Graphics elements

Patrick Biggs
20th April 2015
"""

import abc


class Graph:
    """ Abstract base class from which all graphics object derive"""
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def save(self, file):
        pass

    @abc.abstractmethod
    def to_gcode(self, file):
        pass

    @abc.abstractmethod
    def pick(self, x, y, d):
        pass
    # TODO: Add other export options such as SVG, DXF, PDF, etc.


class Line(Graph):
    """ Concrete class for graphics lines
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def save(self, file):
        file.write("LINE %d, %d, %d, %d\n" % (self.x0, self.y0, self.x1, self.y1))

    def to_gcode(self, file):
        file.write("G0 X%d Yd%\n" % (self.x0, self.y0))  # Move
        file.write("G1 X%d Yd%\n" % (self.x1, self.y1))  # End

    def pick(self, x, y, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""
        d = d*d  # d is distance squared
        # Do Start point
        dx = self.x0 - x
        dy = self.y0 - y
        d2 = dx*dx + dy*dy  # d2 is distance squared avoiding use of sqrt
        if d2 < d:  # if distance <5. Note use of 25 which is 5 squared
            return [self.x0, self.y0]  # return coordinates of start point
        # Do end point
        dx = self.x1 - x
        dy = self.y1 - y
        d2 = dx*dx + dy*dy
        if d2 < d:
            return [self.x1, self.y1]  # return coordinates of end point
        # Do middle point
        mx = int(self.x0 + (self.x1 - self.x0) / 2)  # middle x
        my = int(self.y0 + (self.y1 - self.y0) / 2)  # middle y
        dx = mx - x
        dy = my - y
        d2 = dx*dx + dy*dy
        if d2 < d:
            return [mx, my]  # return coordinates of middle point

        return None  # No matches found


class Circle(Graph):
    """ Concrete class for graphics circles
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def save(self, file):
        file.write("CIRCLE %d, %d, %d\n" % (self.x, self.y, self.r))

    def to_gcode(self, file):
        file.write("(Circle %d, %d radius %d" % (self.x, self.y, self.r))

    def pick(self, x, y, d):
        # TODO: Add code for Circle pick
        return None


class Rectangle(Graph):
    """ Concrete class for graphics rectangles
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        
    def save(self, file):
        file.write("RECTANGLE %d, %d, %d, %d\n" % (self.x0, self.y0, self.x1, self.y1))

    def to_gcode(self, file):
        file.write("G0 X%d Yd%\n" % (self.x0, self.y0))  # Move
        file.write("G1 X%d Yd%\n" % (self.x1, self.y0))  # Right
        file.write("G1 X%d Yd%\n" % (self.x1, self.y1))  # Up
        file.write("G1 X%d Yd%\n" % (self.x0, self.y1))  # Left
        file.write("G1 X%d Yd%\n" % (self.x0, self.y0))  # Down

    def pick(self, x, y, d):
        # TODO: Add code for Rectangle pick
        return None

class Text(Graph):
    """ Concrete class for graphics text
    Based on the MVC architectural pattern so only for data handling, not actually drawing
    """

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def save(self, file):
        file.write("TEXT %d, %d, %s\n" % (self.x, self.y, self.text1))

    def to_gcode(self, file):
        file.write("(Text is %s)\n" % self.text)

    def pick(self, x, y, d):
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

    def save(self, file):
        file.write("GROUP %s\n" % self.name)
        for child in self.children:
            child.save(file)

    def to_gcode(self, file):
        file.write("( Group: %s )\n" % self.name)
        for child in self.children:
            child.to_gcode(file)

    def pick(self, x, y, d):
        for child in self.children:
            r = child.pick(x, y, d)
            if r:  # if there is a find
                return r  # return a the coordinates
        return None  # if no finds then return None

