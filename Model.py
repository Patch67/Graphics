from Graph import Group, Line, Rectangle, Circle

class Model():
    def __init__(self):
        self.__dirty = False
        self.graph = Group("Main")

    def addLine(self, x0, y0, x1, y1):
        self.__graph.add(Line(x0,y0,x1,y1))
        self.setDirty()
    
    def addRectangle(self, x0, y0, x1, y1):
        self.graph.add(Rectangle(x0,y0,x1,y1))
        self.setDirty()

    def addCircle(self,x, y, r):
        self.graph.add(Circle(x, y, r))
        self.setDirty()

    def setDirty(self):
        self.__dirty = True

    def setClean(self):
        self.__dirty = False
        
    def getDirty(self):
        return self.__dirty

