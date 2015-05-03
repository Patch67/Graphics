'''
Patrick Biggs
20th April 2015
'''

'''Graphics Classes'''

import abc


# Abstract Base class
class Graph:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def save(self):
        pass
    
# Concrete Classes
class Line(Graph):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

class Circle(Graph):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

class Rectangle(Graph):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        
class Text(Graph):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        
# Implements the composite pattern
class Group(Graph):
    def __init__(self,name):
        self.name = name
        self.children=[]

    def add(self,graph):
        self.children.append(graph)
