from Graph import Group, Line, Rectangle, Circle
import pickle


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

    @property
    def dirty(self):
        """Getter for __dirty"""
        return self.__dirty

    @dirty.setter
    def dirty(self, dirty):
        """Inform controller by calling controller.dirty_changed"""

        self.__dirty = dirty  # Change value
        self.controller.dirty_changed()  # Notify Controller that value changed

    def add_line(self, x0, y0, x1, y1):
        self.graph.add(Line(x0, y0, x1, y1))
        self.dirty = True
    
    def add_rectangle(self, x0, y0, x1, y1):
        self.graph.add(Rectangle(x0, y0, x1, y1))
        self.dirty = True

    def add_circle(self, x0, y0, x1, y1):
        self.graph.add(Circle(x0, y0, x1, y1))
        self.dirty = True

    def add_poly_line(self):
        # TODO: Add polyline
        pass

    def add_polygon(self):
        # TODO: Add polygon
        pass

    def add_group(self):
        # TODO: Add code for group
        pass

    def add_instance(self, x, y):
        # TODO: Add code for instance
        pass

    def load(self, file):
        """Load the entire Graph Structure
        :param file: The open file object to load from
        :return:
        """
        try:
            self.graph = pickle.load(file)
            self.dirty = False
        except EOFError:
            print("Error could not load %s" % file.name)

    def save(self, file):
        """Save the entire Graph structure
        :param file: The open file object to save to
        """
        try:
            pickle.dump(self.graph, file=file)
            self.dirty = False
        except IOError:
            print("Error could not save %s" % file.name)

    def snap(self, v, d):
        """A pass through method to avoid Controller calling graph.snap directly.
        :param v: Vector2
        :param d: Distance allowed around v
        :return: Either None for no snap or a Marker object if a snap detected
        """
        return self.graph.snap(v, d)