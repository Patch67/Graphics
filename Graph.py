""" Contains Graphics classes based on Compound design pattern

Patrick Biggs
20th April 2015
"""

import abc


# Abstract Base class
class Graph:
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


# Concrete Classes
class Line(Graph):
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


class Circle(Graph):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def save(self, file):
        file.write("CIRCLE %d, %d, %d\n" % (self.x, self.y, self.r))

    def to_gcode(self, file):
        file.write("(Circle %d, %d radius %d" % (self.x, self.y, self.r))


class Rectangle(Graph):
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


class Text(Graph):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def save(self, file):
        file.write("TEXT %d, %d, %s\n" % (self.x, self.y, self.text1))

    def to_gcode(self, file):
        file.write("(Text is %s)\n" % self.text)


# Implements the composite pattern
class Group(Graph):
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
