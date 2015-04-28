from tkinter import *

class View():
    def __init__(self, control, master):
        self.control = control #Allows View to talk to controller
        self.frame = Frame(master, width = 512, height = 512)
        
        # main menu
        menubar = Menu(master)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command = control.cmdNew)
        filemenu.add_command(label="Open", command = control.cmdOpen)
        filemenu.add_command(label="Save", command = control.cmdSave)
        filemenu.add_command(label="Save as", command = control.cmdSaveAs)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = control.cmdExit)
        menubar.add_cascade(label="File", menu = filemenu)

        # edit menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command = control.cmdNull)
        editmenu.add_command(label="Redo", command = control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command = control.cmdNull)
        editmenu.add_command(label="Copy", command = control.cmdNull)
        editmenu.add_command(label="Paste", command = control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Delete", command = control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Select all", command = control.cmdNull)
        menubar.add_cascade(label="Edit", menu = editmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command = control.cmdNull)
        menubar.add_cascade(label="Help", menu = helpmenu)
        
        master.config(menu=menubar)#lock in menubar

        #Set up frame
        #self.frame = Frame(self,)
        self.frame.pack()
        self.frame.focus_set()#enable key events

        self.frame.bind("<Control-o>", self.keyOpen)
        self.frame.bind("<Control-s>", self.keySave)
        
        master.protocol('WM_DELETE_WINDOW', control.cmdExit)#call when window closed

    def messageBox(self,text):
        return messagebox.askquestion("Patrick says",text) == "yes"

    def openFileDialog(self):
        return filedialog.askopenfilename( filetypes = (("Gcode","*.gcode"),("All files","*.*")))

    def saveFileDialog(self, initialFile):
        return filedialog.asksaveasfile(mode='w', initialfile = initialFile, filetypes = (("Gcode","*.gcode"),("All files","*.*")), defaultextension=".gcode")

    def keyOpen(self, e):
        self.control.cmdOpen()

    def keySave(self ,e):
        self.control.cmdOpen()
