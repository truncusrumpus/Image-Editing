from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel.Pixel import Pixel
from Utilities.colours import *

class Tester:
    def __init__(self):
        self.design1("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

    def design1(self, filename):
        colour_list = blue_col_group + red_col_group

        e = Editor()
        e.create_rgba_array(1920, 1080, black)
        p = Painter(e.array, filename)
        colour_list = p.randomize_list(colour_list)

        p.artist6(700, (1, 2), [black])
        for col in colour_list:
            # p.artist70(1000, 1, [col], 300)
            p.artist71(1000, 1, [col], True, 300)

        e.load_array(p.export_array())
        e.save_image(filename)




test = Tester()