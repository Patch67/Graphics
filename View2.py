from Model2 import *

class TextPline(Pline):
	def __init__(self):
		pass
		
	def show(self):
		print("Move %d, %d" % (self.points[0].y, self.points[0].y))
		for c in range(1, size(points)):
			print("Draw %d, %d" % (self.points[c].y, self.points[c].y))
		
class TextRectangle(Rectangle):
	def __init__(self):
		pass
		
	def show(self):
		print("Move %d,%d" % (self.p0.x, self.p0.y))
		


#Test
main=Group("Main")
p0=Vector(0,0)
p1=Vector(10,10)
r=Rectangle(p0,p1)
tr=TextRectangle(r)
tr.show()
main.add(r)
print(r.area())
c=Circle(p0,5)
main.add(c)
c=Circle(p1,5)
main.add(c)
print(c.area())


