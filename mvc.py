'''
tkinter MVC
'''

from tkinter import Tk
from Model import *
from View import *
from TextGraph import TextGroup

class Controller():
    def __init__(self):
        self.root = Tk()
        self.model = Model()
        self.view = View(self,self.root)
        self.appname = ""
        self.filename = ""
        self.stateTools = True
        self.mode = "SELECT"
        self.step = 0
        self.x = 0#Previous click coords
        self.y = 0#Previous click coords
        
    def cmdNew(self):
        if self.model.getDirty():
            self.cmdSave()
        self.model = Model()
        self.filename = ""
        self.setTitle()
            
    
    def cmdOpen(self):
        self.filename = self.view.openFileDialog()
        if self.filename !="":
            self.setTitle()

    def cmdSave(self):
        '''if app already has a filename simply save else do save as'''
        if self.filename != "":
            tg=TextGroup(self.model.graph,sys.stdout)
            tg.show()
        else:
            self.cmdSaveAs()

    def cmdSaveAs(self):
        try:
            file = self.view.saveFileDialog(self.filename)
        except IOError:
            self.view.warningBox(self.appname, "Can't open file %s" % self.filename)
        else:
            if file:#if valid file
                #self.model.save(filename)
                tg=TextGroup(self.model.graph, file)
                tg.show()
                self.filename = file.name
                file.close()
                self.model.setClean()
                self.setTitle()
        

    def cmdExit(self):
        if self.model.getDirty():
            if self.view.questionBox(self.appname, "Do you want to save your work?"):
                self.cmdSave()
        self.root.destroy()#This is tkinter specific

    def cmdToolbar(self):
        self.view.hideToolbar()

    def cmdLeftClick(self, x, y):
        if self.mode == "LINE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                print("Line (%d,%d), (%d,%d)" % (self.x, self.y, x, y))
                self.model.addLine(self.x, self.y, x, y)
                self.x = x
                self.y = y
                self.step = 0
        elif self.mode == "CIRCLE":
            if self.step ==0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                print("Circle (%d, %d), %d" % (self.x, self.y, x))
                self.x = x
                self.y = y
                self.step = 0
        elif self.mode == "RECTANGLE":
            if self.step == 0:
                self.x = x
                self.y = y
                self.step += 1
            else:
                print("Rectangle (%d,%d), (%d,%d)" % (self.x, self.y, x, y))
                self.model.addRectangle(self.x, self.y, x, y)
                self.x = x
                self.y = y
                self.step = 0

    def cmdRightClick(self, x, y):
        #self.view.infoBox("User pressed","x %d, y %d" % (x,y))
        self.view.showContextMenu(x, y)

    def cmdNull(self):
        self.view.infoBox(self.appname, "Not yet implemented")

    def cmdDirty(self):
        self.model.setDirty()
        self.setTitle()

    def cmdClean(self):
        self.model.setClean()
        self.setTitle()

    def cmdTools(self):
        self.stateTools = not(self.stateTools)
        if self.stateTools:
            self.view.showToolBar()
        else:
            self.view.hideToolBar()

    #Drawing Commands
    def cmdLine(self):
        self.mode = "LINE"
        self.step = 0

    def cmdCircle(self):
        self.mode = "CIRCLE"
        self.step = 0
        
    def cmdRectangle(self):
        self.mode = "RECTANGLE"
        self.step = 0

    def getTitle(self):
        if self.model.getDirty():
            title = "*"
        else:
            title = " "
        title += self.appname
        if self.filename != "":
            title += "-" + self.filename
        return title
    
    def setTitle(self):
        self.root.title(self.getTitle())
        
    def run(self):
        self.setTitle()
        self.root.mainloop()#This is tkinter specific

#Main program
controller = Controller()
controller.appname = "My MVC GUI"
controller.run()
