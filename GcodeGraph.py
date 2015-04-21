'''
Patrick Biggs
20th April 2015
'''

'''GCode Graph Decorators'''

from Graph import *

class GcodeLine(Line):
    def __init__(self,line):
        self.line=line
        super(GcodeLine,self).__init__(line.x0,line.y0,line.x1,line.y1)

    def show(self):
        print("G0 X%d Y%d" % (self.x0,self.y0))
        print("G1 X%d Y%d" % (self.x1, self.x0))

class GcodeRectangle(Rectangle):
    def __init__(self,rect):
        self.rect = rect
        super(GcodeRectangle,self).__init__(rect.x0,rect.y0,rect.x1,rect.y1)

    def show(self):
        print("G0 X%d Y%d" % (self.x0,self.y0))
        print("G1 X%d Y%d" % (self.x1, self.y0))
        print("G1 X%d Y%d" % (self.x1, self.y1))
        print("G1 X%d Y%d" % (self.x0, self.y1))
        print("G1 X%d Y%d" % (self.x0,self.y0))


class GcodeGroup(Group):
    def __init__(self,group):
        self.group=group
        super(GcodeGroup,self).__init__(group.name)

    def show(self):
        print("(Group: %s)" % self.name)
        for c in self.group.children:
            type(c)
            if isinstance(c,Line):
                GcodeLine(c).show()
            elif isinstance(c,Rectangle):
                GcodeRectangle(c).show()
            else:
                print("(Not Implemented)")
                type(c)
