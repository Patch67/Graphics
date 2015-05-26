""" Controller """

from Model import *
from View import *
from Marker import EndPointMarker, MidPointMarker, SquareMarker, CentreMarker, InlineMarker
from Vectors import Vector2


class Controller():
    """The business logic of the application."""

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
        self.clicks = []  # A list of clicks, not just one.
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

    '''COMMANDS - Responses to GUI events'''

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
        """Control mouse move events"""
        '''See if mouse snaps to anything'''
        self.view.erase_markers()
        hit = self.model.snap(Vector2(x, y), 20)
        if hit:
            x = hit[1].x
            y = hit[1].y
            if hit[0] == "End":
                self.view.marker_list.append(EndPointMarker(self.view, hit[1]))
            elif hit[0] == "Mid":
                self.view.marker_list.append(MidPointMarker(self.view, hit[1]))
            elif hit[0] == "Centre":
                self.view.marker_list.append(CentreMarker(self.view, hit[1]))
            elif hit[0] == "Inline":
                self.view.marker_list.append(InlineMarker(self.view, hit[1], hit[2]))
        '''Process Construction lines'''
        if self.view.temp:  # if there is a graphics operation in progress
            '''See if the mouse snaps more'''
            v = Vector2(x, y)
            hit = self.view.temp.snap_more(v)
            if hit[0] == "Sqr":
                self.view.marker_list.append(SquareMarker(self.view, hit[1], hit[2]))  # Note 2 coordinates here
            self.view.temp.mouse_move(v)  # tell the graphics operation about the mouse move

    def cmd_left_click(self, mx, my):
        # TODO: Investigate snap controls; Snap_to end_point, mid_point, in_line_with, grid
        """Called when user clicks left mouse button
        Note coordinates are windows relative, so top left corner of window is 0,0 wherever the window is on screen.
        """
        # TODO: Look at making a Mode class to eliminate all these if self.mode clauses
        # TODO: Add code for Select
        print("Mouse click %d, %d" % (mx, my))
        v = Vector2(mx, my)
        '''See if mouse snaps to near object'''
        hit = self.model.snap(v, 20)
        if hit:
            v.x = hit[1].x
            v.y = hit[1].y
            print("Hit at %d, %d" % (v.x, v.y))
        if not self.view.temp:  # If not yet in the construction stage
            self.clicks.append(v)  # Add first click to clicks list
            if self.mode == "LINE":
                self.view.add_temp_line(v)
            elif self.mode == "CIRCLE":
                self.view.add_temp_circle(v)
            elif self.mode == "RECTANGLE":
                self.view.add_temp_rectangle(v)
            elif self.mode == "PLINE":
                self.view.add_temp_pline(v)
        else:  # We are in the construction phase
            self.view.temp.snap_more(v)  # TODO: Bug here. These snaps override model snaps
            self.clicks.append(v)  # There are no more snaps so v can be written to the clicks list
            self.view.erase_markers()
            if self.mode == "LINE":
                self.view.temp.close(v)
                self.view.temp = None  # Kill the temp object
                for click in self.clicks:
                    print("Click %d, %d" % (click.x, click.y))
                self.model.add_line(self.clicks)
                self.clicks = []
            elif self.mode == "CIRCLE":
                self.view.temp.close(v)
                self.view.temp = None  # Kill the temp object
                self.model.add_circle(self.clicks)
                self.clicks = []
            elif self.mode == "RECTANGLE":
                self.view.temp.close(v)
                self.view.temp = None  # Kill the temp object
                self.model.add_rectangle(self.clicks)
                self.clicks = []
            elif self.mode == "PLINE":
                self.view.temp.add_node(v)
        self.x = v.x
        self.y = v.y
        # TODO: Add code for poly line
        # TODO: Add code for polygon

    def cmd_right_click(self, x, y):
        """Show context menu. This depends on the mode we are in"""
        self.right = Vector2(x, y)
        if self.mode == "PLINE":
            self.view.show_pline_context_menu(x, y)
        else:
            self.view.show_context_menu(x, y)  # Show generic context menu

    def cmd_null(self):
        self.view.info_box(self.name, "Not yet implemented")

    def cmd_tools(self):
        """Show / hide the toolbar"""
        self.stateTools = not self.stateTools
        if self.stateTools:
            self.view.show_toolbar()
        else:
            self.view.hide_toolbar()

    '''DRAWING COMMANDS'''
    def cmd_line(self):
        self.mode = "LINE"

    def cmd_circle(self):
        """Sets us up to draw circles"""
        self.mode = "CIRCLE"
        
    def cmd_rectangle(self):
        self.mode = "RECTANGLE"

    def cmd_pline(self):
        self.mode = "PLINE"

    def cmd_pline_close(self):
        self.view.temp.close(True)  # Close pline with the last right click
        self.view.temp = None  # Kill the temp object
        self.model.add_poly_line(self.clicks, True)  # Add pline

    def cmd_pline_end(self):
        self.view.temp.close(False)  # Close pline with the last right click
        self.view.temp = None  # Kill the temp object
        self.model.add_poly_line(self.clicks, False)  # Add pline

    '''MISCELLANEOUS'''
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

'''MAIN PROGRAM'''
controller = Controller("My MVC GUI")  # Construct a controller

