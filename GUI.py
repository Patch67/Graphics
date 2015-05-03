__author__ = 'Patrick'


class Application():
    def __init__(self):
        self.__name = ""
        self.menus = []
        self.toolbars = []

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def create_data_class(self, dir):
        file = open(dir + "\data.py","w")
        file.write("'''The Data Class'''\n")
        file.write("#GUIWikiPy\n")
        file.close()

    def create_GUI_class(self, dir):
        file = open(dir + "\GUI.py","w")
        file.write("'''The GUI Class'''\n")
        file.write("#GUIWikiPy\n")
        file.close()

    def create_command_class(self, dir):
        file = open(dir + "\\command.py","w")
        file.write("'''The Command Class'''\n")
        file.write("#GUIWikiPy\n")
        file.close()

    def create_user_command_class(self, dir):
        file = open(dir + "/User.py","w")
        file.write("'''The User Command Class'''\n")
        file.write("#GUIWikiPy\n")
        file.close()

    def save(self, dir):
        self.create_data_class(dir)
        self.create_GUI_class(dir)
        self.create_command_class(dir)
        self.create_user_command_class(dir)


class Menu():
    def __init__(self):
        self.__name = ""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def write(self, filename):


class Toolbar():
    def __init__(self):
        self.__name = ""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


app = Application()
app.set_name("My Generated Application")
main = Menu()
main.set_name = "Main"
app.menus.append(main)
app.save("C:\GUI_Test")




