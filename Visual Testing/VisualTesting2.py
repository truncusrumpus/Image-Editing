from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel.Pixel import Pixel


class VisualTesting:
    def __init__(self):
        print("MAIN TESTING")
        self.main_testing()

    def main_testing(self):
        # e = Editor()
        # e.create_rgba_array(1000, 800)
        # p = Painter(e.array, "C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")
        colours = []
        for r in range(75, 255, 30):
            colours.append([r, 10, 10, 255])

        # ARTIST 7
        # e = Editor("C:/Users/hughr/Downloads/Images/Image Editing/test_input.png")
        # p = Painter(e.array, "C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")
        # p.convert_col([[255, 255, 255, 255]], [255, 255, 255, 255], True, True, True)
        # p.artist7(1000, 1, colours, 600)
        # p.interpolate(0.6)

        # WEIGHTED RANDOM
        # e = Editor()
        # e.create_rgba_array(10, 10, [0, 0, 0, 255])
        # p = Painter(e.array)
        # test_list = [0, 0]
        # for i in range(10000):
        #     if p.weighted_random_bool(0.3):
        #         test_list[0] += 1
        #     else:
        #         test_list[1] += 1
        # print(test_list[0]/10000)

        e.load_array(p.export_array())
        e.save_image("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")


vt = VisualTesting()
