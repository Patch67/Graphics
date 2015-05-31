"""Temp classes display graphics objects as they are being constructed.
This is in the realms of the View in the MVC framework so no references to Model.
"""
import abc
from Vectors import Vector2


class Temp:
    """Abstract base class for all temporary graphics objects.

    This means anything that is in the process of construction prior to being written to the canvas permanently.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, view, v):
        self.canvas = view.canvas
        self.v0 = v
        self.v1 = None
        self.id = None  # Reference to construction object

    @abc.abstractmethod
    def mouse_move(self, v):
        """Shows the graphics object as it is being created, i.e. as the mouse moves around"""
        pass

    @abc.abstractmethod
    def close(self):
        """Kill the temporary construction object (self.id) and creates the finished article"""
        pass

    def escape(self):
        """Abandons the construction of a graphics object"""
        self.canvas.delete(self.id)


class TempLine(Temp):
    """Class for the construction of a line"""
    def __init__(self, view, v):
        super(TempLine,self).__init__(view, v)

    def mouse_move(self, v):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_line(self.v0.x, self.v0.y, v.x, v.y)  # Create new temp line

    def close(self, v):
        """Kill the temporary construction line and create the finished item"""
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_line(self.v0.x, self.v0.y, v.x, v.y)


class TempRectangle(Temp):
    """Class for the construction of a rectangle"""
    def __init__(self, view, v):
        super(TempRectangle, self).__init__(view, v)

    def mouse_move(self, v):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_rectangle(self.v0.x, self.v0.y, v.x, v.y)  # Create new temp line

    def close(self, v):
        self.v1 = v
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_rectangle(self.v0.x, self.v0.y, self.v1.x, self.v1.y)


class TempOval(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, v):
        super(TempOval, self).__init__(view, v)

    def mouse_move(self, v):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(self.v0.x, self.v0.y, v.x, v.y)  # Create new temp line

    def close(self, v):
        self.canvas.delete(self.id)
        self.id = None
        self.canvas.create_oval(self.v0.x, self.v0.y, v.x, v.y, fill="#476042")

    def snap_more(self, v):
        """Overrides Temp.snap_more
        :param v: v is an referenced object which may well have it's contents altered.
        """
        '''Check if nearly square'''
        width = abs(self.v0.x - v.x)
        height = abs(self.v0.y - v.y)
        if abs(width - height) < 10:
            ave = (width + height) / 2
            self.v1 = v  # Just to initiate a Vector2 variable
            if self.v0.x < v.x:
                self.v1.x = self.v0.x + ave
            else:
                self.v1.x = self.v0.x - ave
            if self.v0.y < v.y:
                self.v1.y = self.v0.y + ave
            else:
                self.v1.y = self.v0.y - ave
            return ["Sqr",self.v0, self.v1]
        else:
            return ["None", v]


class TempCircle(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, v):
        super(TempCircle, self).__init__(view, v)

    def mouse_move(self, v):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        radius = self.v0.distance(v)
        lo = Vector2(self.v0.x - radius, self.v0.y - radius)
        hi = Vector2(self.v0.x + radius, self.v0.y + radius)
        self.id = self.canvas.create_oval(lo.x, lo.y, hi.x, hi.y)  # Create new temp line

    def close(self, v):
        self.canvas.delete(self.id)
        self.id = None
        radius = self.v0.distance(v)
        lo = Vector2(self.v0.x - radius, self.v0.y - radius)
        hi = Vector2(self.v0.x + radius, self.v0.y + radius)
        self.id = self.canvas.create_oval(lo.x, lo.y, hi.x, hi.y)  # Create new temp line



class TempPline(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, v):
        super(TempPline, self).__init__(view, v)
        self.nodes = [v]

    def add_node(self, v):
        self.nodes.append(v)
        self.canvas.create_line(self.nodes[-2].x, self.nodes[-2].y, v.x, v.y)  # Create new temp line

    def mouse_move(self, v):
        # erase old line, if it exists else draw new line
        if self.id:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_line(self.nodes[-1].x, self.nodes[-1].y, v.x, v.y)  # Create new temp line

    def close(self, close):
        """Kill the temporary construction line and create the finished item"""
        self.canvas.delete(self.id)
        self.id = None
        """TODO: This does not seem right.
        We've just deleted one line but are creating multiple lines.
        Shouldn't I just recreate the last line?
        """
        #for i in range(len(self.nodes)-1):  # Exclude the last node
        self.canvas.create_line(self.nodes[-2].x, self.nodes[-2].y, self.nodes[-1].x, self.nodes[-1].y)
        if close:
            self.canvas.create_line(self.nodes[0].x, self.nodes[0].y, self.nodes[-1].x, self.nodes[-1].y)
        self.nodes = []

