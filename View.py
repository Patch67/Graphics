from tkinter import *
from PIL import Image, ImageTk

class View():
    def __init__(self, control, master):
        self.control = control #Allows View to talk to controller
        #self.frame = Frame(master, width = 512, height = 512)
        self.frame = Frame(master)
        master.wm_state('zoomed')# Full screen Possibly doesn't work on Mac
        
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

        # toolbar menus
        
        toolbarmenu = Menu(menubar, tearoff=0)
        check = StringVar()
        toolbarmenu.add_checkbutton(label='Tools', variable=check, onvalue=1, offvalue=0)
        menubar.add_cascade(label="Toolbar", menu = toolbarmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command = control.cmdNull)
        menubar.add_cascade(label="Help", menu = helpmenu)
        
        master.config(menu=menubar)#lock in menubar

        # context menu
        self.context = Menu(master, tearoff=0)
        self.context.add_command(label="Dirty", command=control.cmdDirty)
        self.context.add_command(label="Clean", command=control.cmdClean)

        #Add toolbar
        self.toolbar = Frame(master, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(self.toolbar, image=eimg, bd=1, relief=RAISED, command=control.cmdExit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)
       
        self.toolbar.pack(side=TOP, fill=X)

        #Set up frame
        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.focus_set()#enable key events

        self.frame.bind("<Control-o>", self.keyOpen)
        self.frame.bind("<Control-s>", self.keySave)
        self.frame.bind("<Button-3>", self.rightClick)
        
        self.frame.bind("<Configure>", self.onResize)

        master.protocol('WM_DELETE_WINDOW', control.cmdExit)#call when window closed


        

    def onResize(self,e):
        pass

    def questionBox(self,title, text):
        return messagebox.askquestion(title, text) == "yes"

    def warningBox(self, title, text):
        messagebox.showwarning(title, text)

    def infoBox(self, title, text):
        messagebox.showinfo(title, text)


    def openFileDialog(self):
        return filedialog.askopenfilename( filetypes = (("Gcode","*.gcode"),("All files","*.*")))

    def saveFileDialog(self, initialFile):
        return filedialog.asksaveasfile(mode='w', initialfile = initialFile, filetypes = (("Gcode","*.gcode"),("All files","*.*")), defaultextension=".gcode")

    def keyOpen(self, e):
        self.control.cmdOpen()

    def keySave(self, e):
        self.control.cmdOpen()

    def rightClick(self, e):
        self.control.cmdRightClick(e.x_root, e.y_root)
        
    def showContextMenu(self, x, y):
        self.context.tk_popup(x, y, 0)

    def showToolBar(self):
        self.toolbar.lift(self.master)

    def hideToolbar(self):
        self.toolbar.lower(self.frame)
