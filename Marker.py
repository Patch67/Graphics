__author__ = 'Patrick'

class Marker:
    def __init__(self, view, v):
        self.view = view
        self.v = v
        self.id = None

    def draw(self):
        pass

    def erase(self):
        self.view.canvas.delete(self.id_list)

class EndPointMarker(Marker):
    def __init__(self, view, v):
        super(EndPointMarker, self).__init__(view, v)
        self.draw()

    def draw(self):
        self.view.marker_list.append(self.view.canvas.create_rectangle(self.v.x - 5, self.v.y - 5, self.v.x + 5, self.v.y + 5, outline="#ff0000"))


class MidPointMarker(Marker):
    def __init__(self, view, v):
        super(MidPointMarker, self).__init__(view, v)
        self.draw()

    def draw(self):
        self.view.marker_list.append(self.view.canvas.create_line(self.v.x - 5, self.v.y - 5, self.v.x + 5, self.v.y + 5, fill="#ff0000"))
        self.view.marker_list.append(self.view.canvas.create_line(self.v.x + 5, self.v.y - 5, self.v.x - 5, self.v.y + 5, fill="#ff0000"))