"""Temp classes display graphics objects as they are being constructed.
This is in the realms of the View in the MVC framework so no references to Model.
"""
import abc
from Vectors import Vector2


class Temp:
    """Base class for all temporary graphics objects.

    This means anything that is in the process of construction prior to being written to the canvas permanently.
    """

    def __init__(self, view, v):
        self.view = view
        self.canvas = view.canvas
        self.v0 = v
        self.v1 = None  # TODO: Not every class needs v0 & v2 could have Temp2 parallel to Graph and Graph2
        self.id_list = []  # Reference list of construction object[s]

    def mouse_move(self, v):
        """Shows the graphics object as it is being created, i.e. as the mouse moves around"""
        # Delete Construction object(s)
        # Deal with the mouse move
        # Draw new construction object(s)
        pass

    def close(self):
        """Kill the temporary construction object (self.id) and creates the finished article"""
        # Delete construction object(s)
        self.erase_construction_graphics()
        # reset construction object reference list
        self.id_list = None
        pass

    def erase_construction_graphics(self):
        """Remove all construction objects"""
        for id in self.id_list:
            self.canvas.delete(id)
'''
    def escape(self):
        """Abandons the construction of a graphics object"""
        self.erase_construction_graphics(self.id_list)
'''

class TempLine(Temp):
    """Class for the construction of a line"""
    def __init__(self, view, v):
        super(TempLine,self).__init__(view, v)

    def mouse_move(self, v):
        # erase_construction_graphics old line, if it exists else draw new line
        self.erase_construction_graphics()
        self.id_list = [self.canvas.create_line(self.v0.x, self.v0.y, v.x, v.y)]  # Create new temp line


class TempRectangle(Temp):
    """Class for the construction of a rectangle"""
    def __init__(self, view, v):
        super(TempRectangle, self).__init__(view, v)

    def mouse_move(self, v):
        # erase_construction_graphics old line, if it exists else draw new line
        self.erase_construction_graphics()
        self.id_list = [self.canvas.create_rectangle(self.v0.x, self.v0.y, v.x, v.y)]  # Create new temp line


class TempOval(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, v):
        super(TempOval, self).__init__(view, v)

    def mouse_move(self, v):
        # erase_construction_graphics old line, if it exists else draw new line
        self.erase_construction_graphics()
        self.id_list = [self.canvas.create_oval(self.v0.x, self.v0.y, v.x, v.y)]  # Create new temp line

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
        # erase_construction_graphics old line, if it exists else draw new line
        self.erase_construction_graphics()
        radius = self.v0.distance(v)
        lo = Vector2(self.v0.x - radius, self.v0.y - radius)
        hi = Vector2(self.v0.x + radius, self.v0.y + radius)
        self.id_list = [self.canvas.create_oval(lo.x, lo.y, hi.x, hi.y)]  # Create new temp line


class TempPline(Temp):
    """Class for the construction of a circle"""
    def __init__(self, view, v):
        super(TempPline, self).__init__(view, v)
        self.nodes = [v]

    def add_node(self, v):
        self.nodes.append(v)
        self.canvas.create_line(self.nodes[-2].x, self.nodes[-2].y, v.x, v.y)  # Create new temp line

    def mouse_move(self, v):
        # erase_construction_graphics old line, if it exists else draw new line
        self.erase_construction_graphics()
        self.id_list = [self.canvas.create_line(self.nodes[-1].x, self.nodes[-1].y, v.x, v.y)]  # Create new temp line


class TempPaste(Temp):
    def __init__(self, view, v, paste_buffer):
        super(TempPaste,self).__init__(view, v)
        self.paste_buffer = paste_buffer

    def mouse_move(self, v):
        """Move everything relative to first point"""
        self.erase_construction_graphics()
        offset = Vector2(v.x - self.v0.x, v.y - self.v0.y)
        self.paste_buffer.move(offset)
        self.id_list = self.view.draw_group(self.paste_buffer)
        print("Paste.mouse_move")
        print(self.id_list)

