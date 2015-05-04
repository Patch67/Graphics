"""
tkinter MVC
"""

from tkinter import Tk
from Model import *
from View import *
from TextGraph import TextGroup
import sys


class Controller():
    """This contains the business logic of the application"""

    def __init__(self, name):
        """Constructor"""
        self.root = Tk()
        self.model = Model(self)
        self.view = View(self, self.root)
        self.__name = name
        self.__filename = ""  # Can't use setter here 'cos Python needs to declare __filename member
        self.set_title()  # Call set title because __name & __filename have been changed without setters
        self.stateTools = True
        self.mode = "SELECT"
        self.step = 0
        self.x = 0  # Previous click coords
        self.y = 0  # Previous click coords

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
        self.set_title()  # Every time the application name changes reset the window title

    def get_filename(self):
        return self.__filename

    def set_filename(self, filename):
        self.__filename = filename
        self.set_title()  # Every time the filename changed reset the window title

    def cmd_new(self):
        if self.model.get_dirty():
            self.cmd_save()
        self.model = Model()
        self.set_filename("")
            
    
    def cmd_open(self):
        if self.model.get_dirty():
            '''App has unsaved data so ask user to save it'''
            if self.view.question_box(self.__name, "Do you want to save your work?"):
                self.cmd_save()
        filename = self.view.open_file_dialog()
        if filename != "":
            self.set_filename(filename)

    def cmd_save(self):

        if self.get_filename() != "":  # if app already has a filename simply save else do save as
            TextGroup(self.model.graph,sys.stdout).show()
        else:
            self.cmd_save_as()

    def cmd_save_as(self):
        try:
            file = self.view.save_file_dialog(self.__filename)
        except IOError:
            self.view.warning_box(self.__name, "Can't open file %s" % self.__filename)
        else:
            if file:  # if valid file
                # self.model.save(filename)
                tg=TextGroup(self.model.graph, file)
                tg.show()
                self.set_filename(file.name)
                file.close()
                self.model.set_dirty(False)

    def cmd_dirty(self):
        self.model.set_dirty(True)

    def cmd_clean(self):
        self.model.set_dirty(False)

    def cmd_exit(self):
        if self.model.get_dirty():
            if self.view.question_box(self.__name, "Do you want to save your work?"):
                self.cmd_save()
        self.root.destroy()  # This is tkinter specific

    def cmd_left_click(self, x, y):
        if self.mode == "LINE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                print("Line (%d,%d), (%d,%d)" % (self.x, self.y, x, y))
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
                print("Circle (%d, %d), %d" % (self.x, self.y, x))
                self.x = x
                self.y = y
                self.step = 0
        elif self.mode == "RECTANGLE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                print("Rectangle (%d,%d), (%d,%d)" % (self.x, self.y, x, y))
                self.model.add_rectangle(self.x, self.y, x, y)
                self.x = x
                self.y = y
                self.step = 0

    def cmd_right_click(self, x, y):
        self.view.show_context_menu(x, y)

    def cmd_null(self):
        self.view.info_box(self.__name, "Not yet implemented")

    def dirty_changed(self):
        self.set_title()

    def cmd_tools(self):
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
        if self.model.get_dirty():
            title = "*"
        else:
            title = " "
        title += " " + self.get_name()
        title += " - " + self.get_filename()
        return title
    
    def set_title(self):
        """Sets the title of the Window

        This is tkinter specific and should be in View not controller
        """

        self.root.title(self.get_title())
        
    def run(self):
        """Starts the main program loop

        This is tkinter specific and should be in View not controller
        """
        self.root.mainloop()  # This is tkinter specific

# Main program
controller = Controller("My MVC GUI")
controller.run()
