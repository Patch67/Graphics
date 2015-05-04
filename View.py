from tkinter import Tk, filedialog, Frame, Menu, BOTH, YES, RAISED, Button, TOP, LEFT, Y, messagebox
from PIL import Image, ImageTk


class View():
    """This calls contains all the tkinter specific code"""

    def __init__(self, control):
        """View constructor"""
        self.control = control  # Link back to talk to controller
        self.master = Tk()
        self.master.wm_state('zoomed')  # Full screen. Might not work on Mac
        self.frame = Frame(self.master)

        self.context = None

        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()

        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.focus_set()
        
        self.create_events()

    def run(self):
        """Start tkinter"""
        self.master.mainloop()

    def exit(self):
        self.master.destroy()

    def set_title(self, title):
        """Set Window title"""
        self.master.title(title)

    def create_menus(self):
        """creates the menus"""
        # main menu
        menubar = Menu(self.master)

        # file menus
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="^N",
                             command=self.control.cmd_new)
        filemenu.add_command(label="Open", accelerator="^O",
                             command=self.control.cmd_open)
        filemenu.add_command(label="Save", accelerator="^S",
                             command=self.control.cmd_save)
        filemenu.add_command(label="Save as",
                             command=self.control.cmd_save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",
                             command=self.control.cmd_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # edit menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", accelerator="^Z",
                             command=self.control.cmd_null)
        editmenu.add_command(label="Redo", accelerator="^C",
                             command=self.control.cmd_null)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", accelerator="^X",
                             command=self.control.cmd_null)
        editmenu.add_command(label="Copy", accelerator="^C",
                             command=self.control.cmd_null)
        editmenu.add_command(label="Paste", accelerator="^V"
                             , command=self.control.cmd_null)
        editmenu.add_separator()
        editmenu.add_command(label="Delete",
                             command = self.control.cmd_null)
        editmenu.add_separator()
        editmenu.add_command(label="Select all",
                             command = self.control.cmd_null)
        menubar.add_cascade(label="Edit", menu=editmenu)

        # drawing menus
        drawingmenu = Menu(menubar, tearoff=0)
        drawingmenu.add_command(label="Select",
                                command=self.control.cmd_null)
        drawingmenu.add_command(label="Line",
                                command=self.control.cmd_line)
        drawingmenu.add_command(label="Rectangle",
                                command=self.control.cmd_rectangle)
        drawingmenu.add_command(label="Circle",
                                command=self.control.cmd_circle)
        drawingmenu.add_command(label="Group",
                                command=self.control.cmd_null)
        drawingmenu.add_command(label="Instance",
                                command=self.control.cmd_null)
        menubar.add_cascade(label="Drawing", menu=drawingmenu)

        # toolbar menus
        toolbarmenu = Menu(menubar, tearoff=0)
        toolbarmenu.add_checkbutton(label='Tools',
                                    command=self.control.cmd_tools)
        menubar.add_cascade(label="Toolbar", menu=toolbarmenu)

        # help menus
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About",
                             command = self.control.cmd_null)
        menubar.add_cascade(label="Help", menu = helpmenu)

        self.master.config(menu=menubar)  # lock in menubar


    def create_context_menus(self):
        """Creates the connects menus, i.e. for right click"""
        self.context = Menu(self.master, tearoff=0)
        self.context.add_command(label="Dirty",
                                 command=self.control.cmd_dirty)
        self.context.add_command(label="Clean",
                                 command=self.control.cmd_clean)

    def create_toolbar(self):
        """Creates toolbar, hopefully floating dockable but not yet"""
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(self.toolbar, image=eimg, bd=1,
                            relief=RAISED, command=self.control.cmd_exit)
        exitButton.image = eimg
        exitButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1,
                               relief=RAISED, command=self.control.cmd_null)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1,
                               relief=RAISED, command=self.control.cmd_null)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        self.toolbar.pack(side=LEFT, fill=Y)
        
    def create_events(self):
        """Binds keyboard events to handlers"""
        self.frame.bind("<Control-o>", self.key_open)
        self.frame.bind("<Control-s>", self.key_save)
        self.frame.bind("<Button-1>", self.left_click)
        self.frame.bind("<Button-3>", self.right_click)
        self.frame.bind("<Configure>", self.on_resize)

        # Window closing event
        self.master.protocol('WM_DELETE_WINDOW', self.control.cmd_exit)

    def on_resize(self,e):
        """Called when window changes size"""
        pass

    @staticmethod
    def question_box(title, text):
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        return messagebox.askquestion(title, text) == "yes"

    @staticmethod
    def warning_box(title, text):
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        messagebox.showwarning(title, text)

    @staticmethod
    def info_box(title, text):
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        messagebox.showinfo(title, text)

    @staticmethod
    def open_file_dialog():
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        return filedialog.askopenfilename(filetypes=(("Gcode","*.gcode"), ("All files","*.*")))

    @staticmethod
    def save_file_dialog(initial_file):
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        return filedialog.asksaveasfile(mode='w',
                                        initialfile=initial_file,
                                        filetypes=(("Gcode","*.gcode"),("All files","*.*")),
                                        defaultextension=".gcode")

    def key_open(self, e):
        self.control.cmd_open()

    def key_save(self, e):
        self.control.cmd_open()

    def left_click(self, e):
        self.control.cmd_left_click(e.x_root, e.y_root)


    def right_click(self, e):
        self.control.cmd_right_click(e.x_root, e.y_root)
        
    def show_context_menu(self, x, y):
        self.context.tk_popup(x, y, 0)

    def show_toolbar(self):
        # self.frame = Frame(self.master)

        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()
        self.create_toolbar()
        self.create_toolbar()
        self.frame.pack(fill=BOTH, expand=YES)
        self.frame.focus_set()
        
        self.create_events()

    def hide_toolbar(self):
        self.toolbar.pack_forget()
