""" Controller """

from Model import *
from View import *
from Marker import EndPointMarker, MidPointMarker
from Temp import TempLine, TempCircle, TempRectangle
from Graph import Vector2


class Controller():
    """This contains the business logic of the application"""

    def __init__(self, name):
        """Constructor"""
        self.model = Model(self)
        self.view = View(self)
        self.__name = name
        self.__filename = ""  # Can't use setter here 'cos Python needs to declare __filename member
        self.set_title()  # Call set title because __name & __filename have been changed without setters
        self.stateTools = True
        self.mode = "SELECT"
        self.x = 0  # Previous click coordinates
        self.y = 0  # Previous click coordinates
        self.view.run()  # Start the GUI

    @property
    def name(self):
        return self.__name

    @name.setter
    def set_name(self, name):
        self.__name = name
        self.set_title()  # Every time the application name changes reset the window title

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename
        self.set_title()  # Every time the filename changed reset the window title

    '''System Events'''
    def dirty_changed(self):
        """Called by Model whenever dirty changes"""
        self.set_title()
        self.view.redraw(self.model.graph)  # In tkinter graphics objects are permanent so no need to redraw

    '''Commands - Responses to GUI events'''

    def cmd_new(self):
        if self.model.dirty:
            self.cmd_save()
        self.model = Model(self)
        self.filename = ""
        self.view.clear()

    def cmd_open(self):
        """Controls the process of opening a file


        """
        if self.model.dirty:  # App has unsaved data so ask user to save it
            if self.view.question_box(self.name, "Do you want to save your work?"):
                self.cmd_save()
        filename = self.view.open_file_dialog()
        if filename != "":  # if user does not press Cancel in response to open file dialog
            self.filename = filename
            file = open(filename, mode="rb")
            self.model.load(file)
            self.view.make_group(self.model.graph)
            file.close()

    def cmd_save(self):
        if self.filename != "":  # if app already has a filename simply save else do save as
            file = open(self.filename, "wb")
            self.model.save(file)
            file.close()
        else:
            self.cmd_save_as()

    def cmd_save_as(self):
        try:
            file = self.view.save_file_dialog(self.filename)
        except IOError:
            self.view.warning_box(self.name, "Can't access file %s" % self.filename)
        else:
            if file:  # if valid file
                try:
                    self.model.save(file)
                except:
                    self.view.warning_box(self.name, "Error saving file %s" % self.filename)
                self.filename = file.name
                file.close()
                self.model.dirty = False

    def cmd_exit(self):
        if self.model.dirty:
            if self.view.question_box(self.name, "Do you want to save your work?"):
                self.cmd_save()
        self.view.exit()  # Exit the application

    def cmd_escape(self):
        if self.view.temp:  # if we are in the process of creating an object
            self.view.temp.escape()  # remove any creation artefacts
            self.view.temp = None  # reset creation object

    def mouse_move(self, x, y):
        self.view.erase_markers()
        hit = self.model.graph.snap(Vector2(x,y), 20)
        if hit:
            x = hit[1].x
            y = hit[1].y
            if hit[0] == "End":
                self.view.marker_list.append(EndPointMarker(self.view, hit[1]))
            elif hit[0] == "Mid":
                self.view.marker_list.append(MidPointMarker(self.view, hit[1]))


    def cmd_left_click(self, x, y):
        # TODO: Investigate snap controls; Snap_to end_point, mid_point, in_line_with, grid
        """Called when user clicks left mouse button
        Note coordinates are windows relative, so top left corner of window is 0,0 wherever the window is on screen.
        """
        # TODO: Look at making a Mode class to eliminate all these if self.mode clauses
        # TODO: Add code for Select
        if self.mode == "LINE":
            if not self.view.temp:
                hit = self.model.graph.snap(Vector2(x,y), 20)
                if hit:
                    x = hit[1].x
                    y = hit[1].y
                    if hit[0] == "End":
                        self.view.marker_list.append(EndPointMarker(self.view, hit[1]))
                    elif hit[0] == "Mid":
                        self.view.marker_list.append(MidPointMarker(self.view, hit[1]))
                self.view.temp = TempLine(self.view, self, x, y)  # Create the temp object
                self.x = x
                self.y = y
            else:
                result = self.view.temp.close(x, y)  # Tell view to finish drawing object in progress
                x = result[0]
                y = result[1]
                self.view.erase_markers()
                self.view.temp = None  # Kill the temp object
                self.model.add_line(self.x, self.y, x, y)
                self.x = x
                self.y = y
        elif self.mode == "CIRCLE":
            # TODO: Make circle via centre, radius as well as corner, corner
            if not self.view.temp:
                result = self.model.graph.snap(Vector2(x, y), 20)
                if result:
                    x = result[1].x
                    y = result[1].y
                self.view.temp = TempCircle(self.view, self, x, y)  # Create the temp object
                self.x = x
                self.y = y
            else:
                result = self.view.temp.close(x, y)  # Tell view to finish drawing object in progress
                x = result[0]
                y = result[1]
                self.view.temp = None  # Kill the temp object
                self.model.add_circle(self.x, self.y, x, y)
                self.x = x
                self.y = y
        elif self.mode == "RECTANGLE":
            if not self.view.temp:
                result = self.model.graph.snap(Vector2(x, y), 20)
                if result:
                    x = result[1].x
                    y = result[1].y
                self.view.temp = TempRectangle(self.view, self, x, y)
                self.x = x
                self.y = y
            else:
                self.view.temp.close(x, y)  # Tell view to finish drawing object in progress
                self.view.temp = None  # Kill the temp object
                result = self.model.graph.snap(Vector2(x, y), 20)
                if result:
                    x = result[1].x
                    y = result[1].y
                self.model.add_rectangle(self.x, self.y, x, y)
                self.x = x
                self.y = y
        # TODO: Add code for poly line
        # TODO: Add code for polygon

    def cmd_right_click(self, x, y):
        self.view.show_context_menu(x, y)

    def cmd_null(self):
        self.view.info_box(self.name, "Not yet implemented")

    def cmd_tools(self):
        """Show / hide the toolbar"""
        self.stateTools = not self.stateTools
        if self.stateTools:
            self.view.show_toolbar()
        else:
            self.view.hide_toolbar()

    # Drawing Commands
    def cmd_line(self):
        self.mode = "LINE"

    def cmd_circle(self):
        """Sets us up to draw circles"""
        self.mode = "CIRCLE"
        
    def cmd_rectangle(self):
        self.mode = "RECTANGLE"

    def get_title(self):
        """Makes the title for the Window"""
        if self.model.dirty:
            title = "*"
        else:
            title = " "
        title += " " + self.name
        title += " - " + self.filename
        return title
    
    def set_title(self):
        """Sets the title of the Window"""
        self.view.set_title(self.get_title())

# Main program
controller = Controller("My MVC GUI")  # Construct a controller

