class Graphic():
    """Abstract class to base all grpahics classes on"""
    def __init__(self):
        pass
    def pick(x, y, d):
        pass

    
class Line(Graphic):
    """Concrete implementation of a graphics line class"""
    def __init__(self,x0,y0,x1,y1):
        """Construct line object"""
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


    def pick(self, x, y, d):
        """If start point, end point or mid point is within d units return
        their coordinates.
        if not return None, i.e. no match"""
        d = d*d  # d is distance squared
        # Do Start point
        dx = self.x0 - x
        dy = self.y0 - y
        d2 = dx*dx + dy*dy  # d2 is distance squared avoiding use of sqrt
        if d2 < d:  # if distance <5. Note use of 25 which is 5 squared
            return (self.x0, self.y0)  # return coordinates of start point
        # Do end point
        print("End")
        dx = self.x1 - x
        dy = self.y1 - y
        d2 = dx*dx + dy*dy
        if d2 < d:
            return (self.x1, self.y1)  # return coordinates of end point
        # Do middle point
        mx = self.x0 + (self.x1 - self.x0) / 2  # middle x
        my = self.y0 + (self.y1 - self.y0) / 2 # middle y
        dx = dx - x
        dy = dy - y
        d2 = dx*dx + dy*dy
        if d2 < d:
            return (mx, my)  # return coordinates of middle point
        
        return None
    


l = Line(0,0,100,100)
print(l.pick(2,2,5))
print(l.pick(50,50,5))
print(l.pick(97,97,5))

