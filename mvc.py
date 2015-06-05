""" Controller """

from Model import *
from View import *
from Marker import EndPointMarker, MidPointMarker, SquareMarker, CentreMarker, InlineMarker
from Snap import EndPoint, MidPoint, HorizontalInline, VerticalInline, Centre, Square, Horizontal, Vertical
from Vectors import Vector2


class Controller:
    """The business logic of the application."""

    def __init__(self, name):
        self.model = Model(self)
        self.view = View(self)
        self.__name = name
        self.__filename = ""  # Can't use setter here 'cos Python needs to declare __filename member
        self.set_title()  # Call set title because __name & __filename have been changed without setters
        self.stateTools = True
        self.mode = "SELECT"
        self.clicks = []  # A list of clicks, not just one.
        self.paste_buffer = None
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
        self.view.draw_group(self.model.graph)  # Force redraw

    '''COMMANDS - Responses to GUI events'''

    def cmd_new(self):
        if self.model.dirty:
            self.cmd_save()
        self.model = Model(self)
        self.filename = ""
        self.clicks = []
        self.view.clear_screen()

    def cmd_open(self):
        """Controls the process of opening a file
        """
        if self.model.dirty:  # App has unsaved data so ask user to save it
            if self.view.question_box(self.name, "Do you want to save your work?"):
                self.cmd_save()
        filename = self.view.open_file_dialog()
        if filename != "":  # if user does not press Cancel in response to open file dialog
            self.filename = filename
            self.clicks = []
            file = open(filename, mode="rb")
            self.model.load(file)
            self.view.draw_group(self.model.graph)
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

    def cmd_select_all(self):
        self.model.select_all()

    def cmd_redraw(self):
        self.view.clear_screen()
        self.view.draw_group(self.model.graph)

    def cmd_escape(self):
        self.clicks = []
        if self.view.temp:  # if we are in the process of creating an object
            self.view.temp.erase_construction_graphics()  # remove any creation artefacts
            self.view.temp = None  # reset creation object

    def mouse_move(self, x, y):
        """Control mouse move events"""
        v = Vector2(x,y)
        if self.mode == "SELECT":
            pass
        else:
            '''See if mouse snaps to anything'''
            self.view.erase_markers()
            hit = self.model.snap(self.clicks, v, 20)
            if hit:
                if isinstance(hit, EndPoint):
                    self.view.marker_list.append(EndPointMarker(self.view, hit.v))
                elif isinstance(hit, MidPoint):
                    self.view.marker_list.append(MidPointMarker(self.view, hit.v))
                elif isinstance(hit, VerticalInline) or isinstance(hit, HorizontalInline):
                    self.view.marker_list.append(InlineMarker(self.view, hit.v, hit.v1))
                elif isinstance(hit, Centre):
                    self.view.marker_list.append(CentreMarker(self.view, hit.v))
                elif isinstance(hit, Square):
                    self.view.marker_list.append(SquareMarker(self.view, hit.v, hit.v1))  # Note 2 coordinates here
                elif isinstance(hit, Horizontal):
                    print("Line Horizontal")
                elif isinstance(hit, Vertical):
                    print("Line Vertical")
                if self.mode == "PASTE":
                    print("PASTE")
                    print(self.view.temp)

            if self.view.temp:  # if there is a graphics operation in progress
                self.view.temp.mouse_move(v)  # tell the graphics operation about the mouse move

    def cmd_left_click(self, mx, my):
        """Called when user clicks left mouse button
        Note coordinates are windows relative, so top left corner of window is 0,0 wherever the window is on screen.
        """
        #print("Left click %d, %d" % (mx, my))

        v = Vector2(mx, my)  # Convert windows space coordinates into model space vector
        if self.mode == "SELECT":
            self.selection_list = [self.model.pick(v, 10)]
        elif self.mode == "BOX":
            pass
        else:
            self.clicks.append(v)
            hit = self.model.snap(self.clicks, v, 20)
            if hit:
                v = hit.v
                self.clicks.pop()
                self.clicks.append(v)
            if len(self.clicks) == 1:  # First click
                if self.mode == "LINE":
                    self.view.add_temp_line(v)
                elif self.mode == "CIRCLE":
                    self.view.add_temp_circle(v)
                elif self.mode == "OVAL":
                    self.view.add_temp_oval(v)
                elif self.mode == "RECTANGLE":
                    self.view.add_temp_rectangle(v)
                elif self.mode == "PLINE":
                    self.view.add_temp_pline(v)
                elif self.mode == "PASTE":
                    print("Paste 1st click")
                    self.view.add_temp_paste(v, self.paste_buffer)
            else:  # subsequent click
                self.view.erase_markers()
                if self.mode == "LINE":
                    self.view.temp.close()
                    self.view.temp = None
                    self.model.add_line(self.clicks)
                    self.clicks = []
                elif self.mode == "CIRCLE":
                    self.view.temp.close()
                    self.view.temp = None
                    self.model.add_circle(self.clicks)
                    self.clicks = []
                elif self.mode == "OVAL":
                    self.view.temp.close()
                    self.view.temp = None
                    self.model.add_oval(self.clicks)
                    self.clicks = []
                elif self.mode == "RECTANGLE":
                    self.view.temp.close()
                    self.view.temp = None
                    self.model.add_rectangle(self.clicks)
                    self.clicks = []
                elif self.mode == "PLINE":
                    self.view.temp.add_node(v)
                elif self.mode == "PASTE":
                    print("Paste subsequent click")
                    print(self.paste_buffer)
                    self.view.temp.close()
                    self.view.temp = None
                    self.model.paste(self.paste_buffer)
                    self.clicks = []

    def cmd_right_click(self, x, y):
        """Show context menu. This depends on the mode we are in"""
        if self.mode == "PLINE":
            self.view.show_pline_context_menu(x, y)
        else:
            self.view.show_context_menu(x, y)  # Show generic context menu

    def cmd_left_drag(self, x, y):
        v = Vector2(x,y)
        if self.mode == "SELECT":
            print("Dragging %d, %d" % (v.x, v.y))

    def cmd_left_release(self, x, y):
        #print("End Drag at %d, %d" % (x, y))
        pass

    def cmd_null(self):
        self.view.info_box(self.name, "Not yet implemented")

    def cmd_tools(self):
        """Show / hide the toolbar"""
        self.stateTools = not self.stateTools
        if self.stateTools:
            self.view.show_toolbar()
        else:
            self.view.hide_toolbar()

    '''EDITING COMMANDS'''
    def cmd_cut(self):
        pass

    def cmd_copy(self):
        self.paste_buffer = self.model.get_selected()
        for element in self.paste_buffer.children:
            print(element)

    def cmd_paste(self):
        self.cmd_escape()
        if self.paste_buffer:
            self.mode = "PASTE"

    '''DRAWING COMMANDS'''
    def cmd_select(self):
        self.cmd_escape()
        self.mode = "SELECT"

    def cmd_selection_box(self):
        self.cmd_escape()
        self.mode = "BOX"

    def cmd_line(self):
        self.cmd_escape()
        self.mode = "LINE"

    def cmd_circle(self):
        self.cmd_escape()
        self.mode = "CIRCLE"

    def cmd_oval(self):
        self.cmd_escape()
        self.mode = "OVAL"

    def cmd_rectangle(self):
        self.cmd_escape()
        self.mode = "RECTANGLE"

    def cmd_pline(self):
        self.cmd_escape()
        self.mode = "PLINE"

    def cmd_pline_close(self):
        self.view.temp.close()  # Close pline with the last right click
        self.view.temp = None  # Kill the temp object
        self.model.add_poly_line(self.clicks, True)  # Add pline
        self.clicks = []

    def cmd_pline_end(self):
        self.view.temp.close()  # Close pline with the last right click
        self.view.temp = None  # Kill the temp object
        self.model.add_poly_line(self.clicks, False)  # Add pline
        self.clicks = []

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

