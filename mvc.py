'''
tkinter MVC
'''

from tkinter import *

class Model():
    def __init__(self):
        self.__dirty = False

    def setDirty(self):
        self.__dirty = True

    def getDirty(self):
        return self.__dirty

class View():
    def __init__(self, master):
        self.frame = Frame(master)

class Controller():
    def __init__(self):
        self.root = Tk()
        self.model = Model()
        self.view = View(self.root)

        # main menu
        menubar = Menu(self.root)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command = self.cmdOpen)
        filemenu.add_command(label="Save", command = self.cmdSave)
        filemenu.add_command(label="Save as", command = self.cmdSaveAs)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = self.cmdExit)
        menubar.add_cascade(label="File", menu = filemenu)

        # edit menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command = self.cmdNull)
        editmenu.add_command(label="Redo", command = self.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command = self.cmdNull)
        editmenu.add_command(label="Copy", command = self.cmdNull)
        editmenu.add_command(label="Paste", command = self.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Delete", command = self.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Select all", command = self.cmdNull)
        menubar.add_cascade(label="Edit", menu = editmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command = self.cmdNull)
        menubar.add_cascade(label="Help", menu = helpmenu)
        
        self.root.config(menu=menubar)#lock in menubar
    
    def cmdOpen(self):
        self.filename = filedialog.askopenfilename( filetypes = (("Gcode","*.gcode"),("All files","*.*")))
        if self.filename !="":
            self.setTitle()

    def cmdSave(self):
        '''if app already has a filename simply save else do save as'''
        if self.filename != "":
            pass
            #Put save code here
        else:
            self.cmdSaveAs()

    def cmdSaveAs(self):
        file = filedialog.asksaveasfile()
        self.filename=file.name
        self.setTitle()

    def cmdExit(self):
        self.root.destroy()

    def cmdNull(self):
        pass
        
    def run(self):
        self.root.title("MVC App")
        self.root.mainloop()

#Main program
controller = Controller()
controller.run()
