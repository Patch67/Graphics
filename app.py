from tkinter import Tk, Menu, Frame

class Application(Tk):
    def __init__(self,title):
        super(Application,self).__init__()
        self.title(title)

        # main menu
        menubar = Menu(self)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command = self.cmdOpen)
        filemenu.add_command(label="Save", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        # edit menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=hello)
        editmenu.add_command(label="Copy", command=hello)
        editmenu.add_command(label="Paste", command=hello)
        menubar.add_cascade(label="Edit", menu=editmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=hello)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.config(menu=menubar)#lock in menubar

        self.context = Menu(self, tearoff=0)
        self.context.add_command(label="Beep", command=hello)
        self.context.add_command(label="Exit", command=hello)

        self.myframe = Frame(self, width=512, height=512)
        self.myframe.pack()
        self.myframe.focus_set()
        self.myframe.bind("<Button-3>", self.showContextMenu)
        #self.myframe.bind("<Key>", self.key)


        #Bind keys for commands
        #NB. bind calls method with self and event
        #So we need a method that takes these parameters
        #then simply calls the command method the the menu calls
        
        self.myframe.bind("<Control-o>", self.keyOpen)
        
        
    def showContextMenu(self, e):
        self.context.tk_popup(e.x_root, e.y_root,0)
        
    def keyOpen(self, e):
        self.cmdOpen()

    def cmdOpen(self):
        print("Open")

    def init(self):
        self.grid()
        
def hello():
    print("Hello")
        
app = Application("My App")
app.geometry("250x150+300+300")
#frame = MyFrame(app)
app.mainloop()
