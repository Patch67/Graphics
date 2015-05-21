"""Temp classes display graphics objects as they are being constructed"""
import abc
from Graph import Vector2


class Temp:
    """Abstract base class for all temporary graphics objects.

    This means anything that is in the process of construction prior to being written to the canvas permanently.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, view, controller):
        self.canvas = view.canvas
        self.model = controller.model

    @abc.abstractmethod
    def mouse_move(self, x, y):
        """Shows the grpahics object as it is being created, i.e. as the mouse moves around"""
        pass

    @abc.abstractmethod
    def close(self):
        """Kills the temporary construction and creates the finished article"""
        pass

    def escape(self):
        """Abandons the construction of a graphics object"""
        self.canvas.delete(self.id)


class TempLine(Temp):
    """Class for the construction of a line"""
    def __init__(self, view, controller, x, y):
        super(TempLine,self).__init__(view, controller)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Snap found
            x = result[1].x
            y = result[1].y
        elif abs(self.x0 - x) < 10:  # Near horizontal
            x = self.x0
        elif abs(self.y0 - y) < 10:  # Near vertical
            y = self.y0
        self.id = self.canvas.create_line(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        """Kill the temporary construction line and create the finished item"""
        self.canvas.delete(self.id)
        self.id = None
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Pick found
            x = result[1].x
            y = result[1].y
        elif abs(self.x0 - x) < 10:  # Near horizontal
            x = self.x0
        elif abs(self.y0 - y) < 10:  # Near vertical
            y = self.y0
        self.canvas.create_line(self.x0, self.y0, x, y)
        return [x, y]


class TempRectangle(Temp):
    """Class for the construction of a rectangle"""
    def __init__(self, view, controller, x, y):
        super(TempRectangle, self).__init__(view, controller)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Pick found
            x = result[1].x
            y = result[1].y
        width = abs(self.x0 - x)
        height = abs(self.y0 - y)
        if abs(width - height) < 20:  # Near square
            av = (width + height) / 2
            if self.x0 < x:
                x = self.x0 + av
            else:
                x = self.x0 - av
            if self.y0 < y:
                y = self.y0 + av
            else:
                y = self.y0 - av
        self.id = self.canvas.create_rectangle(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        self.canvas.delete(self.id)
        self.id = None
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Pick found
            x = result[1].x
            y = result[1].y
        self.canvas.create_rectangle(self.x0, self.y0, x, y)
        return [x, y]


class TempCircle(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, controller, x, y):
        super(TempCircle, self).__init__(view, controller)
        self.x0 = x
        self.y0 = y
        self.x1 = None
        self.y1 = None
        self.id = None  # id of temporary line

    def mouse_move(self, x, y):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Pick found
            x = result[1].x
            y = result[1].y
        self.id = self.canvas.create_oval(self.x0, self.y0, x, y)  # Create new temp line

    def close(self, x, y):
        self.canvas.delete(self.id)
        self.id = None
        result = self.model.graph.snap(Vector2(x, y), 20)
        if result:  # Pick found
            x = result[1].x
            y = result[1].y
        self.canvas.create_oval(self.x0, self.y0, x, y)
        return [x, y]