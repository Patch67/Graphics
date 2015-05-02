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

    def __init__(self):
        """Constructor"""
        self.root = Tk()
        self.model = Model()
        self.view = View(self, self.root)
        self.__name = ""
        self.__filename = ""
        self.stateTools = True
        self.mode = "SELECT"
        self.step = 0
        self.x = 0  # Previous click coords
        self.y = 0  # Previous click coords

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def cmd_new(self):
        if self.model.get_dirty():
            self.cmd_save()
        self.model = Model()
        self.__filename = ""
        self.set_title()
            
    
    def cmd_open(self):
        if self.model.get_dirty():
            '''App has unsaved data so ask user to save it'''
            if self.view.question_box(self.__name, "Do you want to save your work?"):
                self.cmd_save()
        self.__filename = self.view.open_file_dialog()
        if self.__filename != "":
            self.set_title()

    def cmd_save(self):

        if self.__filename != "":  # if app already has a filename simply save else do save as
            tg = TextGroup(self.model.graph,sys.stdout)
            tg.show()
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
                self.__filename = file.name
                file.close()
                self.model.set_dirty(False)
                self.set_title()

    def cmd_dirty(self):
        self.cmd_set_dirty(True)

    def cmd_clean(self):
        self.cmd_set_dirty(False)

    def cmd_exit(self):
        if self.model.get_dirty():
            if self.view.question_box(self.__name, "Do you want to save your work?"):
                self.cmd_save()
        self.root.destroy()  # This is tkinter specific

    def cmd_toolbar(self):
        self.view.hide_toolbar()

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
        # self.view.info_box("User pressed","x %d, y %d" % (x,y))
        self.view.show_context_menu(x, y)

    def cmd_null(self):
        self.view.info_box(self.__name, "Not yet implemented")

    def cmd_set_dirty(self, dirty):
        print("Setting dirty ",dirty)
        self.model.set_dirty(dirty)
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
        title += self.__name
        title += " - " + self.__filename
        print("Title is %s" % title)
        return title
    
    def set_title(self):
        self.root.title(self.get_title())
        
    def run(self):
        self.set_title()
        self.root.mainloop()  # This is tkinter specific

# Main program
controller = Controller()
controller.set_name("My MVC GUI")
controller.run()
