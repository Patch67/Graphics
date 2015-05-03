from Graph import Group, Line, Rectangle, Circle


class Model():

    def __init__(self):
        self.__dirty = False
        self.graph = Group("Main")

    def add_line(self, x0, y0, x1, y1):
        self.graph.add(Line(x0,y0,x1,y1))
        self.set_dirty(True)
    
    def add_rectangle(self, x0, y0, x1, y1):
        self.graph.add(Rectangle(x0,y0,x1,y1))
        self.set_dirty(True)

    def add_circle(self,x, y, r):
        self.graph.add(Circle(x, y, r))
        self.set_dirty(True)

    def set_dirty(self, dirty):
        self.__dirty = dirty

    def get_dirty(self):
        return self.__dirty

