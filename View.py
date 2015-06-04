from tkinter import Tk, filedialog, Canvas, Menu, Frame, BOTH, YES, RAISED, Button, TOP, LEFT, Y, messagebox,\
    IntVar, Checkbutton
#from PIL import Image, ImageTk
from Temp import TempLine, TempOval, TempRectangle, TempPline, TempCircle
from Vectors import Vector2

class View:
    """Everything to do with the View from MVC.
    Interfaces with the tkinter environment
    """

    """
    Control methods
    """
    def __init__(self, control):
        """View constructor"""
        self.control = control  # Link back to talk to controller
        self.master = Tk()
        self.master.wm_state('zoomed')  # Full screen. Might not work on Mac
        self.canvas = Canvas(self.master)  # Changed frame to Canvas so I can draw graphics on it.

        self.tool_bar = None  # Holder for tool bar to come later
        self.marker_list = []  # List of marker objects as the result of a snap find
        self.temp = None  # This is for a Temp object when drawing a graphics object is under construction
        self.context = None  # Reference to context menu
        self.pline = None  # Reference to pline context menu

        self.create_menus()
        self.create_context_menus()
        self.create_pline_menu()

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
        edit_menu.add_command(label="Select all", command = self.control.cmd_select_all)
        edit_menu.add_command(label="Redraw", command = self.control.cmd_redraw)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # drawing menus
        drawing_menu = Menu(menu_bar, tearoff=0)
        drawing_menu.add_command(label="Select", command=self.control.cmd_select)
        drawing_menu.add_command(label="Box", command=self.control.cmd_selection_box)
        drawing_menu.add_command(label="Line", command=self.control.cmd_line)
        drawing_menu.add_command(label="Rectangle", command=self.control.cmd_rectangle)
        drawing_menu.add_command(label="Oval", command=self.control.cmd_oval)
        drawing_menu.add_command(label="Circle", command=self.control.cmd_circle)
        drawing_menu.add_command(label="Pline", command=self.control.cmd_pline)
        drawing_menu.add_command(label="Group", command=self.control.cmd_null)
        drawing_menu.add_command(label="Instance", command=self.control.cmd_null)
        menu_bar.add_cascade(label="Drawing", menu=drawing_menu)

        settings_menu = Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Snap", command=self.control.cmd_null)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

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
        self.context.add_command(label="Dirty", command=self.control.cmd_null)
        self.context.add_command(label="Clean", command=self.control.cmd_null)

    def create_pline_menu(self):
        self.pline = Menu(self.master, tearoff=0)
        self.pline.add_command(label="Close", command=self.control.cmd_pline_close)
        self.pline.add_command(label="End", command=self.control.cmd_pline_end)

    def create_events(self):
        """Binds keyboard events to handlers"""
        self.canvas.bind("<Control-o>", self.key_open)
        self.canvas.bind("<Control-s>", self.key_save)
        self.canvas.bind("<Control-a>", self.key_select_all)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<Escape>", self.key_escape)
        self.canvas.bind("<Key>", self.on_key)
        self.canvas.bind('<B1-Motion>', self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
        self.master.protocol('WM_DELETE_WINDOW', self.control.cmd_exit) # Window closing event

    """
    EVENTS
    """
    def on_move(self, e):
        """Called when mouse moves"""
        self.control.mouse_move(e.x, e.y)

    def key_escape(self, e):
        self.control.cmd_escape()

    def on_key(self, e):
        if e.char == "l":
            self.control.cmd_line()
        elif e.char == "r":
            self.control.cmd_rectangle()
        elif e.char == "c":
            self.control.cmd_circle()
        elif e.char == "p":
            self.control.cmd_pline()

    def on_left_drag(self, e):
        self.control.cmd_left_drag(e.x, e.y)

    def on_left_release(self, e):
        self.control.cmd_left_release(e.x, e.y)

    def on_resize(self, e):
        """Called when window changes size"""
        pass

    def key_open(self, e):
        self.control.cmd_open()

    def key_save(self, e):
        self.control.cmd_open()

    def key_select_all(self, e):
        self.control.cmd_select_all()

    def left_click(self, e):
        self.control.cmd_left_click(e.x, e.y)  # e.x & e.y are canvas relative

    def right_click(self, e):
        self.control.cmd_right_click(e.x_root, e.y_root)  # e.x_root & e.y_root are screen relative

    """
    STANDARD DIALOGS
    """
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

    """
    MENU EVENTS
    """
    def show_context_menu(self, x, y):
        self.context.tk_popup(x, y, 0)

    def show_pline_context_menu(self, x, y):
        self.pline.tk_popup(x, y, 0)

    def show_toolbar(self):
        pass

    def hide_toolbar(self):
        pass

    """
    View methods to draw Graph objects
    """
    def erase_markers(self):
        for marker_id in self.marker_list:
            self.canvas.delete(marker_id)

    def draw_line(self, line):
        """Add a new, permanent, line to canvas"""
        if line.selected:
            colour = "blue"
        else:
            colour = "black"
        self.canvas.create_line(line.v0.x, line.v0.y, line.v1.x, line.v1.y, fill=colour)
        self.temp = None  # Clear the temp object.

    def draw_oval(self, oval):
        """Add a new, permanent, oval to canvas"""
        if oval.selected:
            colour = "blue"
        else:
            colour = "black"

        self.canvas.create_oval(oval.v0.x, oval.v0.y, oval.v1.x, oval.v1.y, outline=colour)
        self.temp = None  # Clear the temp object.

    def draw_circle(self, circle):
        """Add a new, permanent, circle to canvas"""

        lo = Vector2(circle.centre.x - circle.radius, circle.centre.y - circle.radius)
        hi = Vector2(circle.centre.x + circle.radius, circle.centre.y + circle.radius)
        if circle.selected:
            colour = "blue"
        else:
            colour = "black"

        self.canvas.create_oval(lo.x, lo.y, hi.x, hi.y, outline=colour)  # Create new temp line
        self.temp = None  # Clear the temp object.

    def draw_rectangle(self, rectangle):
        """Add a new, permanent, rectangle to canvas"""
        if rectangle.selected:
            colour = "blue"
        else:
            colour = "black"

        self.canvas.create_rectangle(rectangle.v0.x, rectangle.v0.y, rectangle.v1.x, rectangle.v1.y, outline=colour)
        self.temp = None  # Clear the temp object.

    def draw_pline(self, pline):
        """Add a new, permanent, pline to canvas"""
        start = pline.nodes[0]
        temp = start
        if pline.selected:
            colour = "blue"
        else:
            colour = "black"

        for i in range(1, len(pline.nodes)):
            node = pline.nodes[i]
            self.canvas.create_line(temp.x, temp.y, node.x, node.y, fill=colour)
            temp = node
        if pline.close:
            self.canvas.create_line(node.x, node.y, start.x, start.y, fill=colour)
        self.temp = None  # Clear the temp object.

    def draw_group(self, group):
        self.clear()
        for child in group.children:
            t = type(child).__name__
            if t == "Line":
                self.draw_line(child)
            elif t == "Oval":
                self.draw_oval(child)
            elif t == "Circle":
                self.draw_circle(child)
            elif t == "Rectangle":
                self.draw_rectangle(child)
            elif t == "Pline":
                self.draw_pline(child)
        self.temp = None  # Clear the temp object.

    def clear(self):
        self.canvas.delete("all")
        self.temp = None

    """
    Set up temporary construction objects
    """
    def add_temp_line(self, v):
        """Adds a new line construction object
        :param v: The start vector
        """
        self.temp = TempLine(self, v)

    def add_temp_rectangle(self, v):
        self.temp = TempRectangle(self, v)

    def add_temp_oval(self,v):
        self.temp = TempOval(self, v)

    def add_temp_circle(self,v):
        self.temp = TempCircle(self, v)

    def add_temp_pline(self, v):
        self.temp = TempPline(self, v)