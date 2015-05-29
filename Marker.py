"""Markers are to display where snap points have been located.
They are use to show to user what type of snap point is available as the mouse moves around the scene.
Markers are part of the View, i.e. they interact with View elements such as canvas, no references to Model.
"""

__author__ = 'Patrick'


class Marker:
    """Base class for all markers"""
    def __init__(self, view, v0):
        self.view = view
        self.v0 = v0
        self.colour = "#ff0000"

    def erase(self):
        self.view.canvas.delete(self.id_list)


class EndPointMarker(Marker):
    """Marks and end point with a little red rectangle"""
    def __init__(self, view, v0):
        super(EndPointMarker, self).__init__(view, v0)
        self.view.marker_list.append(self.view.canvas.create_rectangle(self.v0.x - 5, self.v0.y - 5, self.v0.x + 5, self.v0.y + 5, outline=self.colour))


class MidPointMarker(Marker):
    """Marks a mid point with a little red cross"""
    def __init__(self, view, v0):
        super(MidPointMarker, self).__init__(view, v0)
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x - 5, self.v0.y - 5, self.v0.x + 5, self.v0.y + 5, fill=self.colour))
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x + 5, self.v0.y - 5, self.v0.x - 5, self.v0.y + 5, fill=self.colour))


class CentreMarker(Marker):
    """Marks a little red circle at the centre"""
    def __init__(self, view, v0):
        super(CentreMarker, self).__init__(view, v0)
        self.view.marker_list.append(self.view.canvas.create_oval(self.v0.x - 5, self.v0.y - 5, self.v0.x + 5, self.v0.y + 5, fill=self.colour))


class InlineMarker(Marker):
    """Marks red line between matching model point and snapped cursor position"""
    def __init__(self, view, v0, v1):
        super(InlineMarker, self).__init__(view, v0)
        self.v1 = v1
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x, self.v0.y, self.v1.x , self.v1.y, fill=self.colour))


class SquareMarker(Marker):
    """Marks red line diagonal between fist point and snapped cursor position"""
    def __init__(self, view, v0, v1):
        super(SquareMarker, self).__init__(view, v0)
        self.v1 = v1
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x, self.v0.y, self.v1.x , self.v1.y, fill=self.colour))


class Horizontal(Marker):
    """Marks red line between matching model point and snapped cursor position"""
    def __init__(self, view, v0, v1):
        super(InlineMarker, self).__init__(view, v0)
        self.v1 = v1
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x, self.v0.y, self.v1.x , self.v1.y, fill=self.colour))


class Vertical(Marker):
    """Marks red line between matching model point and snapped cursor position"""
    def __init__(self, view, v0, v1):
        super(InlineMarker, self).__init__(view, v0)
        self.v1 = v1
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x, self.v0.y, self.v1.x , self.v1.y, fill=self.colour))

class Square(Marker):
    """Marks red line between matching model point and snapped cursor position"""
    def __init__(self, view, v0, v1):
        super(Square, self).__init__(view, v0)
        self.v1 = v1
        self.view.marker_list.append(self.view.canvas.create_line(self.v0.x, self.v0.y, self.v1.x , self.v1.y, fill=self.colour))