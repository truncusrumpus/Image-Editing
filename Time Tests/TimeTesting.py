import timeit
from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel.Pixel import Pixel


class TimeTesting:
    def __init__(self):
        print("TIMING INITIALISE EDITOR")
        self.timing_initialise_editor()
        print("TIMING CREATE RGBA ARRAY")
        self.timing_create_rgba_array()
        print("TIMING INITIALISE PAINTER")
        self.timing_initialise_painter()
        print("TIMING FORMAT ARRAY")
        self.timing_format_array()
        print("TIMING EXPORT ARRAY")
        self.timing_export_array()
        print("TIMING OLD CURVE CENTRE")
        self.timing_old_curve_centre()
        print("TIMING CURVE CENTRE")
        self.timing_curve_centre()

    def timing_initialise_editor(self):
        start_time = timeit.default_timer()

        e = Editor()

        time_taken = timeit.default_timer() - start_time

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_create_rgba_array(self):
        e = Editor()

        start_time = timeit.default_timer()
        e.create_rgba_array(3840, 2160)
        time_taken = timeit.default_timer() - start_time

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_initialise_painter(self):
        e = Editor()
        e.create_rgba_array(3840, 2160)

        start_time = timeit.default_timer()

        p = Painter([[None]])

        time_taken = timeit.default_timer() - start_time

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_format_array(self):
        e = Editor()
        e.create_rgba_array(3840, 2160)
        p = Painter([[None]])

        start_time = timeit.default_timer()

        p.format_array(e.array)

        time_taken = timeit.default_timer() - start_time

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_export_array(self):
        e = Editor()
        e.create_rgba_array(3840, 2160)
        p = Painter(e.array)

        start_time = timeit.default_timer()

        p.export_array()

        time_taken = timeit.default_timer() - start_time

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_painting_setup(self):
        start_time = timeit.default_timer()

        e = Editor()
        e.create_rgba_array(3840, 2160)
        p = Painter(e.array)

        time_taken = timeit.default_timer() - start_time
        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_straight_line(self):
        e = Editor()
        e.create_rgba_array(1000, 1000)
        p = Painter(e.array)

    def timing_old_curve_centre(self):
        e = Editor()
        e.create_rgba_array(2000, 2000)
        p = Painter(e.array)

        start_time = timeit.default_timer()

        index = 0
        centre = p.array[0][0]
        upper = 16
        for i in range(1, upper):
            start = Pixel(0, index)
            p.old_curve_centre(start, centre, 1, [i / upper * 255, 20, 20, 255], i)
            index = 2**i

        time_taken = timeit.default_timer() - start_time

        e.load_array(p.export_array())
        e.save_image("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

        print("Time Taken: {0:4.4f}".format(time_taken))

    def timing_curve_centre(self):
        e = Editor()
        e.create_rgba_array(2000, 2000)
        p = Painter(e.array)

        start_time = timeit.default_timer()

        index = 0
        centre = p.array[0][0]
        upper = 16
        for i in range(1, upper):
            start = Pixel(0, index)
            p.curve_centre(start, centre, 1, [20, 20, i / upper * 255, 255], i)
            index = 2**i

        time_taken = timeit.default_timer() - start_time

        e.load_array(p.export_array())
        e.save_image("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

        print("Time Taken: {0:4.4f}".format(time_taken))


time_testing = TimeTesting()

