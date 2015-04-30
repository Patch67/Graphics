from tkinter import *
from PIL import Image, ImageTk

class View():
    def __init__(self, control, master):
        
        self.control = control #Link back to talk to controller
        self.master = master
        master.wm_state('zoomed')# Full screen. Might not work on Mac
        self.frame = Frame(master)

        self.createMenus()
        self.createContextMenus()
        self.createToolBar()

        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.focus_set()
        
        self.createEvents()

    def createMenus(self):
        # main menu
        menubar = Menu(self.master)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="^N",
                             command = self.control.cmdNew)
        filemenu.add_command(label="Open", accelerator="^O",
                             command = self.control.cmdOpen)
        filemenu.add_command(label="Save", accelerator="^S",
                             command = self.control.cmdSave)
        filemenu.add_command(label="Save as",
                             command = self.control.cmdSaveAs)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",
                             command = self.control.cmdExit)
        menubar.add_cascade(label="File", menu = filemenu)

        # edit menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", accelerator="^Z",
                             command = self.control.cmdNull)
        editmenu.add_command(label="Redo", accelerator="^C",
                             command = self.control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", accelerator="^X",
                             command = self.control.cmdNull)
        editmenu.add_command(label="Copy", accelerator="^C",
                             command = self.control.cmdNull)
        editmenu.add_command(label="Paste", accelerator="^V"
                             , command = self.control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Delete",
                             command = self.control.cmdNull)
        editmenu.add_separator()
        editmenu.add_command(label="Select all",
                             command = self.control.cmdNull)
        menubar.add_cascade(label="Edit", menu = editmenu)

        # drawing menus
        drawingmenu = Menu(menubar, tearoff=0)
        drawingmenu.add_command(label="Select",
                                command=self.control.cmdNull)
        drawingmenu.add_command(label="Line",
                                command=self.control.cmdLine)
        drawingmenu.add_command(label="Rectangle",
                                command=self.control.cmdRectangle)
        drawingmenu.add_command(label="Circle",
                                command=self.control.cmdCircle)
        drawingmenu.add_command(label="Group",
                                command=self.control.cmdNull)
        drawingmenu.add_command(label="Instance",
                                command=self.control.cmdNull)
        menubar.add_cascade(label="Drawing", menu = drawingmenu)
                                

        # toolbar menus
        toolbarmenu = Menu(menubar, tearoff=0)
        toolbarmenu.add_checkbutton(label='Tools',
                                    command=self.control.cmdTools)
        menubar.add_cascade(label="Toolbar", menu = toolbarmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About",
                             command = self.control.cmdNull)
        menubar.add_cascade(label="Help", menu = helpmenu)

        self.master.config(menu=menubar)#lock in menubar

    def createContextMenus(self):
        self.context = Menu(self.master, tearoff=0)
        self.context.add_command(label="Dirty",
                                 command=self.control.cmdDirty)
        self.context.add_command(label="Clean",
                                 command=self.control.cmdClean)        

    def createToolBar(self):
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(self.toolbar, image=eimg, bd=1,
                            relief=RAISED, command=self.control.cmdExit)
        exitButton.image = eimg
        exitButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1,
                               relief=RAISED, command=self.control.cmdNull)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1,
                               relief=RAISED, command=self.control.cmdNull)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        
       
        self.toolbar.pack(side=LEFT, fill=Y)
        
    def createEvents(self):
        self.frame.bind("<Control-o>", self.keyOpen)
        self.frame.bind("<Control-s>", self.keySave)
        self.frame.bind("<Button-1>", self.leftClick)
        self.frame.bind("<Button-3>", self.rightClick)
        self.frame.bind("<Configure>", self.onResize)

        #Window closing event
        self.master.protocol('WM_DELETE_WINDOW', self.control.cmdExit)

    def onResize(self,e):
        pass

    def questionBox(self,title, text):
        return messagebox.askquestion(title, text) == "yes"

    def warningBox(self, title, text):
        messagebox.showwarning(title, text)

    def infoBox(self, title, text):
        messagebox.showinfo(title, text)

    def openFileDialog(self):
        return filedialog.askopenfilename(filetypes=(("Gcode","*.gcode"), ("All files","*.*")))

    def saveFileDialog(self, initialFile):
        return filedialog.asksaveasfile(mode='w',
                                        initialfile = initialFile, filetypes = (("Gcode","*.gcode"),("All files","*.*")), defaultextension=".gcode")

    def keyOpen(self, e):
        self.control.cmdOpen()

    def keySave(self, e):
        self.control.cmdOpen()

    def leftClick(self, e):
        self.control.cmdLeftClick(e.x_root, e.y_root)


    def rightClick(self, e):
        self.control.cmdRightClick(e.x_root, e.y_root)
        
    def showContextMenu(self, x, y):
        self.context.tk_popup(x, y, 0)

    def showToolBar(self):
        #self.frame = Frame(self.master)

        self.createMenus()
        self.createContextMenus()
        self.createToolBar()
        self.createToolBar()
        self.createToolBar()
        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.focus_set()
        
        self.createEvents()

    def hideToolBar(self):
        self.toolbar.pack_forget()
