import Graph

class TextLine(Line):
    def __init__(self):
        pass

    def show(self):
        print("LINE((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1))

class TextRectangle(Rectangle):
    def __init__(self):
        pass

    def show(self):
        print("RECTANGLE((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1))

class TextCircle(Circle):
    def __init__(self):
        pass

    def show(self):
        print("CIRCLE((%d, %d), %d)" % (self.x, self.y, self.r))

class TextGroup(Group):
    def __init__(self):
        pass

    def show(self):
        print("GROUP(%s)" % self.name)
        for child in self.children:
            print(child.__type__)
