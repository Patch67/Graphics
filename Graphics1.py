'''
Patrick Biggs
20th April 2015
'''

'''
Example of using two design patterns:-

- Composite pattern - for graphics objects and groups of graphics objects
- Decorator pattern - for displaying graphics objects as text or Gcode

Also note the three modules: -

- Graph - The raw data classes for all graphics objects
- TextGraph - A wrapper providing text output for each concrete member of Graph
- Gcodegraph - A wapper providing Gcode output for each concrete meber of Graph

This setup provides a really good basis to develop a graphics application
It is properly object oriented.

'''
import sys
from Graph import *
from TextGraph import *
from GcodeGraph import *

f=open("Test.txt","w")
#f=sys.stdout

l=Line(0,0,100,100)

#Use Decorators to display line in different ways
TextLine(l).show(f)#Display text
GcodeLine(l).show()#Display gcode

#Make a group
g=Group("My Group")
g.add(l)
g.add(Circle(50,50,50))
g.add(Rectangle(25,25,75,75))
g.add(Text(0,0,"Hello World"))

TextGroup(g,f).show()#Display group using Text Decorators
GcodeGroup(g).show()

print("Hello",file=f)
f.close()


