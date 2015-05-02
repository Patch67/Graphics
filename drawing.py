from tkinter import Tk, Canvas, Frame, BOTH


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.x = 0
        self.y = 0
        
        self.parent = parent        
        parent.bind("<Motion>", self.onMove)
        parent.bind("<Button-1>", self.leftClick)
        parent.bind("<Button-3>", self.rightClick)
        self.parent.title("Colors")        
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0")
        self.canvas.create_rectangle(150, 10, 240, 80, outline="#f50", fill="#f50")
        self.canvas.create_rectangle(270, 10, 370, 80, outline="#05f", fill="#05f")            
        self.canvas.pack(fill=BOTH, expand=1)
        self.inMotion = False
        self.line = 0#Holder for temp line whilst dragging mouse around

    def onMove(self, e):
        if self.inMotion:
            self.canvas.delete(self.line)
            self.line = self.canvas.create_line(self.x, self.y, e.x, e.y)

    def leftClick(self, e):
        if not(self.inMotion):
            self.canvas.create_line(self.x, self.y, e.x, e.y)
        self.x = e.x
        self.y = e.y
        self.inMotion = True

    def rightClick(self, e):
        self.inMotion = False
 


  
root = Tk()
ex = Example(root)
root.geometry("400x100+300+300")
root.mainloop()  
