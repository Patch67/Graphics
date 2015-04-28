'''
tkinter MVC
'''

from tkinter import Tk
from Model import *
from View import *

class Controller():
    def __init__(self):
        self.root = Tk()
        self.model = Model()
        self.view = View(self,self.root)
        self.appname = ""
        self.filename = ""

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
            pass
            #Put save code here
            #self.model.save(filename)
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
                self.filename = file.name
                file.close()
                self.model.setClean()
                self.setTitle()
        

    def cmdExit(self):
        if self.model.getDirty():
            if self.view.questionBox(self.appname, "Do you want to save your work?"):
                self.cmdSave()
        self.root.destroy()#This is tkinter specific

    def cmdRightClick(self, x, y):
        self.view.infoBox("User pressed","x %d, y %d" % (x,y))
        self.view.showContextMenu(x, y)

    def cmdNull(self):
        self.view.infoBox(self.appname, "Not yet implemented")

    def cmdDirty(self):
        self.model.setDirty()
        self.setTitle()

    def cmdClean(self):
        self.model.setClean()
        self.setTitle()
    
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
