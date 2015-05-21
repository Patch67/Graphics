from tkinter import Tk, filedialog, Canvas, Menu, Frame, BOTH, YES, RAISED, Button, TOP, LEFT, Y, messagebox, ARC
from PIL import Image, ImageTk


class View():
    """This calls contains all the tkinter specific code"""

    def __init__(self, control):
        """View constructor"""
        self.control = control  # Link back to talk to controller
        self.master = Tk()
        self.master.wm_state('zoomed')  # Full screen. Might not work on Mac
        self.canvas = Canvas(self.master)  # Changed frame to Canvas so I can draw graphics on it.

        self.tool_bar = None  # Holder for tool bar to come later
        self.temp = None  # This is for a Temp object when drawing a graphics object is under construction
        self.context = None

        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()

        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.focus_set()
        
        self.create_events()

    def run(self):
        """Start the application (tkinter)"""
        self.master.mainloop()

    def exit(self):
        """Quit the application"""
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
        # TODO: Add more options such as cut, copy, paste, rotate, scale, etc.
        self.context.add_command(label="Dirty", command=self.control.cmd_dirty)
        self.context.add_command(label="Clean", command=self.control.cmd_clean)

    def create_toolbar(self):
        """Creates toolbar"""
        # TODO: Make this a floating, dockable tool bar with a menu option to show / hide
        # TODO: Make config file to save current status, Floating, Hidden, Dock_top, dock_bottom, dock_left, dock_right
        self.tool_bar = Frame(self.master, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exit_button = Button(self.tool_bar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_exit)
        exit_button.image = eimg
        exit_button.pack(side=TOP, padx=2, pady=2)

        another_button = Button(self.tool_bar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_null)
        another_button.image = eimg
        another_button.pack(side=TOP, padx=2, pady=2)

        another_button = Button(self.tool_bar, image=eimg, bd=1, relief=RAISED, command=self.control.cmd_null)
        another_button.image = eimg
        another_button.pack(side=TOP, padx=2, pady=2)

        self.tool_bar.pack(side=LEFT, fill=Y)
        
    def create_events(self):
        """Binds keyboard events to handlers"""
        self.canvas.bind("<Control-o>", self.key_open)
        self.canvas.bind("<Control-s>", self.key_save)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<Escape>", self.key_escape)
        self.canvas.bind("<Key>", self.on_key)
        self.master.protocol('WM_DELETE_WINDOW', self.control.cmd_exit) # Window closing event

    def on_resize(self, e):
        """Called when window changes size"""
        pass

    def on_move(self, e):
        """Called when mouse moves"""
        if self.temp:  # if there is a graphics operation in progress
            self.temp.mouse_move(e.x, e.y)  # tell the graphics operation about the mouse move

    def key_escape(self, e):
        self.control.cmd_escape()

    def on_key(self, e):
        if e.char == "l":
            self.control.cmd_line()
        elif e.char == "r":
            self.control.cmd_rectangle()
        elif e.char == "c":
            self.control.cmd_circle()




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
        return filedialog.askopenfilename(filetypes=(("PyCAD","*.cad"), ("All files","*.*")))

    @staticmethod
    def save_file_dialog(initial_file):
        """Just a wrapped for tkinter so command calls can be tkinter independent"""
        return filedialog.asksaveasfile(mode='wb',
                                        initialfile=initial_file,
                                        filetypes=(("PyCAD", "*.cad"),("All files", "*.*")),
                                        defaultextension=".cad")

    def key_open(self, e):
        self.control.cmd_open()

    def key_save(self, e):
        self.control.cmd_open()

    def left_click(self, e):
        self.control.cmd_left_click(e.x, e.y)  # e.x & e.y are canvas relative

    def right_click(self, e):
        self.control.cmd_right_click(e.x_root, e.y_root)  # e.x_root & e.y_root are screen relative
        
    def show_context_menu(self, x, y):
        self.context.tk_popup(x, y, 0)

    def show_toolbar(self):
        # TODO: Make this tool bar open in the right place every time, not just the first time
        self.create_menus()
        self.create_context_menus()
        self.create_toolbar()
        self.create_toolbar()
        self.create_toolbar()
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.focus_set()
        self.create_events()

    def hide_toolbar(self):
        self.tool_bar.pack_forget()

    ''' View methods to draw Graph objects'''

    def redraw(self, graph):
        """In tkinter redraw is not needed because canvas graphics are permanent
        In an application with transient graphics we would need to redraw all the objects
        but tkinter canvas does this for us
        """
        self.temp = None
        pass  # Do nothing

    def make_line(self, line):
        """Add a new, permanent, line to canvas"""
        self.canvas.create_line(line.v0.x, line.v0.y, line.v1.x, line.v1.y, fill="#476042")
        self.temp = None  # Clear the temp object.

    def make_circle(self, circle):
        """Add a new, permanent, circle to canvas"""
        self.canvas.create_oval(circle.v0.x, circle.v0.y, circle.v1.x, circle.v1.y)
        self.temp = None  # Clear the temp object.

    def make_rectangle(self, rectangle):
        """Add a new, permanent, rectangle to canvas"""
        self.canvas.create_rectangle(rectangle.v0.x, rectangle.v0.y, rectangle.v1.x, rectangle.v1.y)
        self.temp = None  # Clear the temp object.

    def clear(self):
        self.canvas.delete(self.canvas.find_all())

    def make_group(self, group):
        self.clear()
        for child in group.children:
            t = type(child).__name__
            if t == "Line":
                self.make_line(child)
            elif t == "Circle":
                self.make_circle(child)
            elif t == "Rectangle":
                self.make_rectangle(child)
            # TODO: Add more options when more graphics objects are available
        self.temp = None  # Clear the temp object.


