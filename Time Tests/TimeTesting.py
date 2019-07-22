import timeit
from Editor.Editor import Editor
from Painter.Painter import Painter


class TimeTesting:
    def __init__(self):
        pass

    def timing_straight_line(self):
        e = Editor()
        e.create_rgba_array(1000, 1000)
        p = Painter(e.array)
        p.straight_line(p.array[0])