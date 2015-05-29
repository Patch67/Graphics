__author__ = 'Patrick'

class Snap:
    def __init__(self, v):
        self.v = v


class EndPoint(Snap):
    def __init__(self, v, distance):
        super(EndPoint, self).__init__(v)
        self.distance = distance


class MidPoint(Snap):
    def __init__(self, v, distance):
        super(MidPoint, self).__init__(v)
        self.distance = distance


class Centre(Snap):
    def __init__(self, v, distance):
        super(Centre, self).__init__(v)
        self.distance = distance


class VerticalInline(Snap):
    def __init__(self, v, v1, distance):
        super(VerticalInline, self).__init__(v)
        self.v1 = v1
        self.distance = distance


class HorizontalInline(Snap):
    def __init__(self, v, v1, distance):
        super(HorizontalInline, self).__init__(v)
        self.v1 = v1
        self.distance = distance


class Square(Snap):
    def __init__(self, v, v1, distance):
        super(Square, self).__init__(v)
        self.v1 = v1
        self.distance = distance


class Horizontal(Snap):
    def __init__(self, v, v1, distance):
        super(Horizontal, self).__init__(v)
        self.v1 = v1
        self.distance = distance


class Vertical(Snap):
    def __init__(self, v, v1, distance):
        super(Vertical, self).__init__(v)
        self.v1 = v1
        self.distance = distance