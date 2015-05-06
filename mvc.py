""" Controller """

from Model import *
from View import *
from TextGraph import TextGroup
import sys


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
        self.step = 0
        self.x = 0  # Previous click coords
        self.y = 0  # Previous click coords
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

    '''Commands - Responses to GUI events'''

    def cmd_new(self):
        if self.model.dirty:
            self.cmd_save()
        self.model = Model(self)
        self.filename = ""

    def cmd_open(self):
        if self.model.dirty:  # App has unsaved data so ask user to save it

            if self.view.question_box(self.name, "Do you want to save your work?"):
                self.cmd_open()
        filename = self.view.open_file_dialog()
        if filename != "":  # if user does not press Cancel in response to open file dialog
            self.filename = filename
            '''Open file code goes here'''

    def cmd_save(self):
        if self.filename != "":  # if app already has a filename simply save else do save as
            TextGroup(self.model.graph,sys.stdout).show()
        else:
            self.cmd_save_as()

    def cmd_save_as(self):
        try:
            file = self.view.save_file_dialog(self.filename)
        except IOError:
            self.view.warning_box(self.name, "Can't access file %s" % self.filename)
        else:
            if file:  # if valid file
                # self.model.save(filename)
                TextGroup(self.model.graph, file).show()
                self.filename = file.name
                file.close()
                self.model.dirty = False

    def cmd_exit(self):
        if self.model.dirty:
            if self.view.question_box(self.name, "Do you want to save your work?"):
                self.cmd_save()
        self.view.exit()  # Exit the application

    def cmd_dirty(self):
        """Called from context menu"""
        self.model.dirty = True

    def cmd_clean(self):
        """Called from context menu"""
        self.model.dirty = False

    def cmd_left_click(self, x, y):
        """Called when user clicks left mouse button"""
        if self.mode == "LINE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                self.model.add_line(self.x, self.y, x, y)
                self.x = x
                self.y = y
                self.step = 0
        elif self.mode == "CIRCLE":
            if self.step ==0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                self.x = x
                self.y = y
                self.step = 0
        elif self.mode == "RECTANGLE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                self.model.add_rectangle(self.x, self.y, x, y)
                self.x = x
                self.y = y
                self.step = 0

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
        self.step = 0

    def cmd_circle(self):
        self.mode = "CIRCLE"
        self.step = 0
        
    def cmd_rectangle(self):
        self.mode = "RECTANGLE"
        self.step = 0

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
controller.view.run()  # Start the GUI
