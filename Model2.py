import math

class Graphic():
	def __init__(self):
		pass
		
class Vector(Graphic):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
class Pline(Graphic):
	def __init__(self):
		self.points = []
		
	def add(self, point):
		self.points.append(point)
	
class Group(Graphic):
	def __init__(self, name):
		self.name = name
		self.graphics = []
		
	def add(self, graphic):
		self.graphics.append(graphic)
		
class Instance(Graphic):
	def __init__(self, name, point):
		self.name = name
		self.point = point
		

class Circle(Graphic):
	def __init__(self, centre, radius):
		self.centre = centre
		self.radius = radius
		
	def circumference(self):
		return 2 * math.pi * self.radius
		
	def area(self):
		return math.pi * self.radius * self.radius
		
class Rectangle(Graphic):
	def __init__(self, p0, p1):
		self.p0 = p0
		self.p1 = p1
		
	def area(self):
		return (self.p1.x - self.p0.x) * (self.p1.y - self.p0.y)

