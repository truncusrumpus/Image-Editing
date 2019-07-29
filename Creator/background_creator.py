from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel.Pixel import Pixel

class Tester:
    def __init__(self):
        self.test()

    def test(self):
        filename = "C:/Users/hughr/Downloads/Images/Image Editing/test_input.png"
        colours = [[73, 133, 230, 255], [31, 40, 135, 255], [15, 23, 102, 255], [32, 70, 140, 255],
                   [10, 48, 120, 255], [54, 145, 224, 255], [54, 153, 224, 255]]

        e = Editor(filename)
        p = Painter(e.array, filename)

        p.artist5(5000, (1, 1), colours, 1200, [[255, 255, 255, 255], 1])

        e.load_array(p.export_array())
        e.save_image(filename)


test = Tester()