class Model():
    def __init__(self):
        self.__dirty = True

    def setDirty(self):
        self.__dirty = True

    def getDirty(self):
        return self.__dirty

