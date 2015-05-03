from Graph import Group, Line, Rectangle, Circle


class Model():
    """The Model part of MVC.

    This is where the data lives.

    The two elements that must be present are controller and dirty.
    Other elements, such as graph, can be added by the programmer to expand capabilities.
    """

    def __init__(self, controller):
        """Model Constructor"""
        '''For any application'''
        self.controller = controller
        self.__dirty = False
        '''For graphics application'''
        self.graph = Group("Main")

    def set_dirty(self, dirty):
        """Setter for dirty

        If dirt has changed will inform controller
        by calling controller.dirty_changed
        """

        if dirty != self.__dirty:
            self.controller.dirty_changed()
        self.__dirty = dirty

    def get_dirty(self):
        """Getter for __dirty"""
        return self.__dirty

    def add_line(self, x0, y0, x1, y1):
        self.graph.add(Line(x0,y0,x1,y1))
        self.set_dirty(True)
    
    def add_rectangle(self, x0, y0, x1, y1):
        self.graph.add(Rectangle(x0,y0,x1,y1))
        self.set_dirty(True)

    def add_circle(self,x, y, r):
        self.graph.add(Circle(x, y, r))
        self.set_dirty(True)


