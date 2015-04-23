from tkinter import Tk, Menu, Frame

class Application(Tk):
    def __init__(self,title):
        super(Application,self).__init__()
        self.title(title)

        # main menu
        menubar = Menu(self)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=hello)
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
        self.context.add_command(label="Beep", command=self.on3)
        self.context.add_command(label="Exit", command=self.on3)

        self.myframe = Frame(self, width=512, height=512)
        self.myframe.pack()
        self.myframe.bind("<Button-3>", self.showContextMenu)
        
    def showContextMenu(self, e):
        print("Button 3")
        self.context.tk_popup(e.x_root, e.y_root,0)
       

    def on3(self):
        print("Hello")

    def init(self):
        self.grid()
        
def hello():
    print("Hello")
        
app = Application("My App")
app.geometry("250x150+300+300")
#frame = MyFrame(app)
app.mainloop()
