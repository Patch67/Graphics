from Graph import Group, Line, Rectangle, Circle, Oval, Pline
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

    def add_line(self, nodes):
        self.graph.add(Line(nodes[0], nodes[1]))
        self.dirty = True

    def add_rectangle(self, nodes):
        self.graph.add(Rectangle(nodes[0], nodes[1]))
        self.dirty = True

    def add_circle(self, nodes):
        self.graph.add(Circle(nodes[0], nodes[0].distance(nodes[1])))
        self.dirty = True

    def add_oval(self, nodes):
        self.graph.add(Oval(nodes[0], nodes[1]))
        self.dirty = True

    def add_poly_line(self, nodes, close):
        self.graph.add(Pline(nodes, close))
        self.dirty = True

    def add_polygon(self):
        # TODO: Add polygon
        pass

    def add_group(self):
        # TODO: Add code for group
        pass

    def add_instance(self):
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

    def select_all(self):
        self.graph.select_all()
        self.dirty = True

    def snap(self, clicks, v, d):
        """A pass through method to avoid Controller calling graph.snap directly.
        :param v: Vector2
        :param d: Distance allowed around v
        :return: Either None for no snap or a Marker object if a snap detected
        """
        return self.graph.snap(clicks, v, d)

    def pick(self, v, d):
        return self.graph.pick(v, d)