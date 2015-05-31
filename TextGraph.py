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
        f.write("Line (%d, %d) - (%d, %d)\n" % (self.x0, self.y0, self.x1, self.y1))


class TextOval(Oval):
    def __init__(self,circle):
        self.circle=circle
        super(TextOval,self).__init__(circle.x,circle.y,circle.r)

    def show(self,f):
        f.write("Circle (%d, %d) - %d\n" % (self.x, self.y, self.r))


class TextRectangle(Rectangle):
    def __init__(self,rectangle):
        self.rectangle = rectangle
        super(TextRectangle,self).__init__(
            rectangle.x0,rectangle.y0,rectangle.x1,rectangle.y1)

    def show(self,f):
        f.write("Rectangle (%d, %d) - (%d, %d)\n" % (self.x0, self.y0, self.x1, self.y1))


class TextText(Text):
    def __init__(self,text):
        self.text = text
        super(TextText,self).__init__(text.x, text.y, text.text)

    def show(self,f):
        f.write("Text (%d, %d) - %s\n" % (self.x, self.y, self.text))


class TextGroup(Group):
    def __init__(self,group,f):
        self.group=group
        self.f=f
        super(TextGroup,self).__init__(group.name)

    def show(self):
        self.f.write("Group: %s\n" % self.name)
        for c in self.group.children:
            if isinstance(c,Line):
                TextLine(c).show(self.f)
            elif isinstance(c,Oval):
                TextOval(c).show(self.f)
            elif isinstance(c,Rectangle):
                TextRectangle(c).show(self.f)
            elif isinstance(c,Text):
                TextText(c).show(self.f)
            else:
                f.write("Not Implemented\n")
                type(c)

