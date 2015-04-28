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
        file = self.view.saveFileDialog(self.filename)
        if file:#if valid file
            #self.model.save(filename)
            self.filename = file.name
            self.setTitle()
            file.close()

    def cmdExit(self):
        if self.model.getDirty():
            if self.view.messageBox("Do you want to save your work?"):
                self.cmdSave()
        self.root.destroy()

    def cmdNull(self):
        pass
    
    def getTitle(self):
        title = self.appname
        if self.filename != "":
            title += "-" + self.filename
        return title
    
    def setTitle(self):
        self.root.title(self.getTitle())
        
    def run(self):
        self.setTitle()
        self.root.mainloop()

#Main program
controller = Controller()
controller.appname = "My MVC GUI"
controller.run()
