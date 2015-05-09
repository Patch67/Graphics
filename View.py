from tkinter import Tk, filedialog, Canvas, Menu, Frame, BOTH, YES, RAISED, Button, TOP, LEFT, Y, messagebox
from PIL import Image, ImageTk
from Graph import *

class View():
    """This calls contains all the tkinter specific code"""

    def __init__(self, control):
        """View constructor"""
        self.control = control  # Link back to talk to controller
        self.master = Tk()
        self.master.wm_state('zoomed')  # Full screen. Might not work on Mac
        self.canvas = Canvas(self.master)  # Changed frame to Canvas so I can draw graphics on it.

        self.context = None

        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()

        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.focus_set()
        
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
        menu_bar = Menu(self.master)

        # file menus
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="^N", command=self.control.cmd_new)
        file_menu.add_command(label="Open", accelerator="^O", command=self.control.cmd_open)
        file_menu.add_command(label="Save", accelerator="^S", command=self.control.cmd_save)
        file_menu.add_command(label="Save as", command=self.control.cmd_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.control.cmd_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # edit menus
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="^Z", command=self.control.cmd_null)
        edit_menu.add_command(label="Redo", accelerator="^C", command=self.control.cmd_null)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="^X", command=self.control.cmd_null)
        edit_menu.add_command(label="Copy", accelerator="^C", command=self.control.cmd_null)
        edit_menu.add_command(label="Paste", accelerator="^V", command=self.control.cmd_null)
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete", command = self.control.cmd_null)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select all", command = self.control.cmd_null)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # drawing menus
        drawing_menu = Menu(menu_bar, tearoff=0)
        drawing_menu.add_command(label="Select", command=self.control.cmd_null)
        drawing_menu.add_command(label="Line", command=self.control.cmd_line)
        drawing_menu.add_command(label="Rectangle", command=self.control.cmd_rectangle)
        drawing_menu.add_command(label="Circle", command=self.control.cmd_circle)
        drawing_menu.add_command(label="Group", command=self.control.cmd_null)
        drawing_menu.add_command(label="Instance", command=self.control.cmd_null)
        menu_bar.add_cascade(label="Drawing", menu=drawing_menu)

        # toolbar menus
        tool_bar_menu = Menu(menu_bar, tearoff=0)
        tool_bar_menu.add_checkbutton(label='Tools', command=self.control.cmd_tools)
        menu_bar.add_cascade(label="Toolbar", menu=tool_bar_menu)

        # help menus
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command = self.control.cmd_null)
        menu_bar.add_cascade(label="Help", menu = help_menu)

        '''Experimental toolbar stuff'''
        x_tools = Menu(menu_bar, tearoff=1)
        x_tools.add_command(label="Select", command=self.control.cmd_null)
        x_tools.add_command(label="Line", command=self.control.cmd_line)
        x_tools.add_command(label="Rectangle", command=self.control.cmd_rectangle)
        x_tools.add_command(label="Circle", command=self.control.cmd_circle)
        x_tools.add_command(label="PLine", command=self.control.cmd_null)
        x_tools.add_command(label="Group", command=self.control.cmd_null)
        x_tools.add_command(label="Instance", command=self.control.cmd_null)
        menu_bar.add_cascade(label = "Tools", menu = x_tools)

        self.master.config(menu=menu_bar)  # lock in menu_bar


    def create_context_menus(self):
        """Creates the connects menus, i.e. for right click"""
        self.context = Menu(self.master, tearoff=0)
        self.context.add_command(label="Dirty", command=self.control.cmd_dirty)
        self.context.add_command(label="Clean", command=self.control.cmd_clean)

    def create_toolbar(self):
        """Creates toolbar, hopefully floating dockable but not yet"""
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(self.toolbar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_exit)
        exitButton.image = eimg
        exitButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_null)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        anotherButton = Button(self.toolbar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_null)
        anotherButton.image = eimg
        anotherButton.pack(side=TOP, padx=2, pady=2)

        self.toolbar.pack(side=LEFT, fill=Y)
        
    def create_events(self):
        """Binds keyboard events to handlers"""
        self.canvas.bind("<Control-o>", self.key_open)
        self.canvas.bind("<Control-s>", self.key_save)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Motion>", self.on_move)
        self.master.protocol('WM_DELETE_WINDOW', self.control.cmd_exit) # Window closing event

    def on_resize(self, e):
        """Called when window changes size"""
        pass

    def on_move(self, e):
        """Called when mouse moves"""
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
                                        filetypes=(("Text","*.txt"),("Gcode","*.gcode"),("All files","*.*")),
                                        defaultextension=".txt")

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
        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()
        self.create_toolbar()
        self.create_toolbar()
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.focus_set()
        self.create_events()

    def hide_toolbar(self):
        self.toolbar.pack_forget()

    ''' View methods to draw Graph objects'''
    def temp_line(self, temp_line):
        pass

    def draw_line(self, line):
        self.canvas.create_line([line.x0, line.y0, line.x1, line.y1])

    def temp_circle(self, circle):
        pass

    def draw_circle(self, circle):
        self.canvas.create_arc([circle.x, circle.y, circle.x + circle.r, circle.y], 0, 360)

    def temp_rectangle(self, temp_rectangle):
        pass

    def draw_rectangle(self, rectangle):
        pass

    def temp_group(self, temp_group):
        pass

    def draw_group(self, group):
        for child in group.children:
            t = (type(child).__name__)
            if t == "Line":
                self.draw_line(child)
            elif t == "Circle":
                self.draw_circle(child)
            elif t == "Rectangle":
                self.draw_rectangle(child)


