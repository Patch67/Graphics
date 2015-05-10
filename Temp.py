import abc


class Temp():
    """Abstract base class for all temporary graphics objects.

    This means anything that is in the process of construction prior to being written to the canvas permanently.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, view):
        self.canvas = view.canvas

    @abc.abstractmethod
    def mouse_move(self, x, y):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class TempLine(Temp):
    """Class for the construction of a line"""
    def __init__(self, view, x, y):
        super(TempLine,self).__init__(view)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)

        self.id = self.canvas.create_line(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_line(self.x0, self.y0, x, y)


class TempRectangle(Temp):
    """Class for the construction of a rectangle"""
    def __init__(self, view, x, y):
        super(TempRectangle, self).__init__(view)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)

        self.id = self.canvas.create_rectangle(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_rectangle(self.x0, self.y0, x, y)


class TempCircle(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, x, y):
        super(TempCircle, self).__init__(view)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)

        self.id = self.canvas.create_oval(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_oval(self.x0, self.y0, x, y)