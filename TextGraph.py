'''
Patrick Biggs
20th April 2015
'''

'''Graph Text Decorator Classes'''

from Graph import *

class TextLine(Line):
    def __init__(self,line):
        self.line=line
        super(TextLine,self).__init__(line.x0,line.y0,line.x1,line.y1)

    def show(self,f):
        f.writeline("Line (%d, %d) - (%d, %d)" % (self.x0, self.y0, self.x1, self.y1))

class TextCircle(Circle):
    def __init__(self,circle):
        self.circle=circle
        super(TextCircle,self).__init__(circle.x,circle.y,circle.r)

    def show(self,f):
        f.writeline("Circle (%d, %d) - %d" % (self.x, self.y, self.r))

class TextRectangle(Rectangle):
    def __init__(self,rectangle):
        self.rectangle = rectangle
        super(TextRectangle,self).__init__(
            rectangle.x0,rectangle.y0,rectangle.x1,rectangle.y1)

    def show(self,f):
        f.writeline("Rectangle (%d, %d) - (%d, %d)" % (self.x0, self.y0, self.x1, self.y1))

class TextText(Text):
    def __init__(self,text):
        self.text = text
        super(TextText,self).__init__(text.x, text.y, text.text)

    def show(self,f):
        f.writeline("Text (%d, %d) - %s" % (self.x, self.y, self.text))

class TextGroup(Group):
    def __init__(self,group,f):
        self.group=group
        self.f=f
        super(TextGroup,self).__init__(group.name)

    def show(self):
        print("Group: %s" % self.name,self.f)
        for c in self.group.children:
            type(c)
            if isinstance(c,Line):
                TextLine(c).show(self.f)
            elif isinstance(c,Circle):
                TextCircle(c).show(self.f)
            elif isinstance(c,Rectangle):
                TextRectangle(c).show(self.f)
            elif isinstance(c,Text):
                TextText(c).show(self.f)
            else:
                f.writeline("Not Implemented")
                type(c)

