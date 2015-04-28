class Model():
    def __init__(self):
        self.__dirty = False

    def setDirty(self):
        self.__dirty = True

    def setClean(self):
        self.__dirty = False
    def getDirty(self):
        return self.__dirty

