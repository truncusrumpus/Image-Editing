from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel.Pixel import Pixel


class VisualTesting:
    def __init__(self):
        print("MAIN TESTING")
        self.main_testing()

    def main_testing(self):
        colour = [255, 0, 0, 255]
        # colours = [colour, [0, 255, 0, 255], [0, 0, 255, 255]]
        colours = [colour]
        e = Editor()
        e.create_rgba_array(200, 200)
        p = Painter(e.array, "C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

        # STRAIGHT LINE
        # start = p.array[2][1]
        # end = p.array[8][4]
        # p.straight_line(start, end, colour, 1)

        # CIRCLE FILL
        # centre = p.array[-20][-20]
        # p.circle_fill(centre, 8, colour)
        # # centre = p.array[180][20]
        # # p.circle_fill(centre, 8, colour)

        # RANDOM LINES
        # start = timeit.default_timer()
        # p.random_lines(200)
        # print(timeit.default_timer() - start)

        # CURVE CENTRE
        # start = p.array[100][100]
        # centre = Pixel(100, 96, False)
        # # centre = p.array[100][90]
        # p.curve_centre(start, centre, 1, colour, 2)

        # CURVE RADIUS
        # centre = Pixel(100, 96, False)
        # centre = p.array[100][100]
        # p.curve_radius(centre, 50, False, 0.5, colour, 2)

        # RANDOM CURVES
        # p.random_curves(40, 2, 300, None)

        # PAINT FILL:
        # Testing with Straight Line Outline
        # coords = [[50, 50], [150, 40], [140, 150], [40, 140], [50, 50]]
        # for i in range(len(coords) - 1):
        #     colour = [i * 30 % 255, i * 30 % 255, 255, 255]
        #     p.straight_line(p.array[coords[i][0]][coords[i][1]], p.array[coords[i + 1][0]][coords[i + 1][1]], colour, 1)
        # Testing with Curve Centre Outline
        # curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1)
        # start = Pixel(50, 100)
        # centre = Pixel(100, 100)
        # p.curve_centre2(start, centre, 1, colour, 2)
        # p.paint_fill(p.array[100][100], [255, 255, 255, 255], [0, 0, 0, 255])

        # PAINT DROP LINE
        # start = p.array[20][60]
        # end = p.array[180][180]
        # p.paint_drop_line(start, end, colour, 2, 15)

        # PAINT DROP CURVE CENTRE
        # start = p.array[51][100]
        # centre = Pixel(88, 100, False)
        # # centre = p.array[100][90]
        # p.paint_drop_curve_centre(start, centre, 0.5, colour, (1, 50))

        # GRID
        # p.grid(20, 20, [0, 255, 0, 255], 1)

        # PAINT FILL CANVAS SKIP
        # p.paint_fill_canvas_skip(colours, [0, 0, 0, 255], (1, 18))

        # ARTIST 5
        # p.artist5(100, (0, 0), colours, 1200, [[0, 0, 0, 255], 1], False)

        # INVERT RGBA IMAGE COLOURS
        # e = Editor("C:/Users/hughr/Downloads/Images/Image Editing/test_input.png")
        # p = Painter(e.array)
        # p.invert_rgba_image_col()

        # STRAIGHT LINE CONTROLLED
        # e = Editor("C:/Users/hughr/Downloads/Images/Image Editing/test_input.png")
        # p = Painter(e.array, "C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")
        # start = Pixel(0, 0)
        # end = Pixel(1060, 510)
        # p.straight_line_controlled(start, end, colour)

        e.load_array(p.export_array())
        e.save_image("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")


vt = VisualTesting()
