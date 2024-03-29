import unittest
import math
from Editor.Editor import Editor
from Painter import Painter
from Pixel.Pixel import Pixel
import timeit

class TestPainter(unittest.TestCase):
    def test_get_item(self):
        test_array = [[1, 10], [2, 20], [3, 30]]

        p = Painter(test_array)
        self.assertEqual(p[0][0].colour, 1)
        self.assertEqual(p[1][2].colour, 30)

    def test_set_item(self):
        test_array = [[1, 10], [2, 20], [3, 30]]

        p = Painter(test_array)
        self.assertEqual(p[0][0].colour, 1)

        # Testing set item using property
        p[0][0].colour = "changed"
        self.assertEqual(p[0][0].colour, "changed")

        # Testing set item not using property
        p[0][0] = "changed"
        self.assertEqual(p[0][0], "changed")

    def test_format_array(self):
        e = Editor()
        test_array = [[0, 1, 2, 3], [0, 1, 2, 3]]
        e.array = test_array
        p = Painter(e.array)

        for w in range(p.width):
            for h in range(p.height):
                self.assertEqual(p.array[w][h].x, w)
                self.assertEqual(p.array[w][h].y, h)

    def test_export_array(self):
        e = Editor("Test_Image_1.png")
        p = Painter(e.array)
        export = p.export_array()
        for w in range(len(export)):
            for h in range(len(export[0])):
                self.assertTrue(all(export[w][h] == e.array[w][h]))

    def test_list_equal(self):
        # Checking list equal returns True for two identical lists
        p = Painter([[None]])
        list1 = [0, -10, 1.1, "x"]
        list2 = [0, -10, 1.1, "x"]
        self.assertTrue(p.list_equal(list1, list2))

        # Checking list equal returns False for two different lists
        list2.append(False)
        self.assertFalse(p.list_equal(list1, list2))

        # Checking list equal returns True for a tuple and a list with same values
        tuple1 = (0, -10, 1.1, "x")
        self.assertTrue(p.list_equal(list1, tuple1))

    def test_list_avg(self):
        p = Painter([[None]])

        list = [1, 2, 3]
        self.assertEqual(p.list_avg(list), 2)
        self.assertEqual(p.list_avg(list), 0.1)

    def test_interpolate_pixel(self):
        nine_pixels = [[None, None, None], [None, None, None], [None, None, None]]
        for x in range(3):
            for y in range(3):
                nine_pixels[x][y] = Pixel(x, y, [30*(x+y), 30*(x+y), 30*(x+y), 255])

        nine_pixels[2][2].colour = [160, 160, 160, 255]
        p = Painter([[None]])
        p.array = nine_pixels
        p.interpolate_pixel(nine_pixels[1][1], 0.8)

        self.assertEqual(nine_pixels[1][1].colour, [61, 61, 61, 255])

        nine_pixels[0][0].colour = False
        nine_pixels[0][1].colour = False
        nine_pixels[0][2] = False
        nine_pixels[1][0].colour = [200, 0, 0, 255]
        nine_pixels[1][1].colour = [60, 60, 60, 255]

        p.array = nine_pixels
        p.interpolate_pixel(nine_pixels[1][1], 0.8)

        self.assertEqual(nine_pixels[1][1].colour, [72, 64, 64, 255])

    def test_list_diff_avg(self):
        p = Painter([[None]])

        list = [1, 2, 4, 7]
        self.assertEqual(p.list_diff_avg(list), 2)

        list = [-0.1, 0.1, 0.4]
        self.assertEqual(p.list_diff_avg(list), 0.25)

    def test_old_curve_centre(self):
        colour = [255, 0, 0, 255]
        e = Editor()
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = p.array[100][100]
        coords = [2000, 1000, 500, 200, 150, 120, 110, 105, 101, 99, 95, 90, 80, 50, 20, 0, -10, -100, -200, -2000]
        for coord in coords:
            centre = Pixel(coord, coord, False)
            p.curve_centre(start, centre, 1, colour, 2)
            e.load_array(p.export_array())
            e.save_image("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

    def test_dist_2d(self):
        p = Painter([[None]])
        self.assertEqual(p.dist_2d(1, 1, 1, 2), 1)
        self.assertEqual(p.dist_2d(1, 1, 2, 2), math.sqrt(2))

    def test_straight_line(self):
        colour = [255, 0, 0, 255]
        e = Editor()

        # Testing horizontal straight line
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = p.array[10][10]
        end = p.array[190][10]
        p.straight_line(start, end, colour)

        assert p.array[10][10].colour == colour
        assert p.array[40][10].colour == colour
        assert p.array[100][10].colour == colour
        assert p.array[160][10].colour == colour
        assert p.array[190][10].colour == colour

        # Testing vertical straight line
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = p.array[10][10]
        end = p.array[10][190]
        p.straight_line(start, end, colour)

        assert p.array[10][10].colour == colour
        assert p.array[10][40].colour == colour
        assert p.array[10][100].colour == colour
        assert p.array[10][160].colour == colour
        assert p.array[10][190].colour == colour

        # Testing diagonal straight line - top left to bottom right
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = p.array[10][10]
        end = p.array[190][190]
        p.straight_line(start, end, colour, 5)

        assert p.array[10][10].colour == colour
        assert p.array[100][100].colour == colour
        assert p.array[190][190].colour == colour

        # Testing diagonal straight line - bottom left to top right
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = p.array[10][130]
        end = p.array[130][10]
        p.straight_line(start, end, colour, 5)

        assert p.array[10][130].colour == colour
        assert p.array[50][90].colour == colour
        assert p.array[90][50].colour == colour
        assert p.array[130][10].colour == colour

        # Testing straight line outside bounds - diagonal
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        start = Pixel(-10, -10, False)
        end = p.array[80][80]
        p.straight_line(start, end, colour, 5)

        assert p.array[20][20].colour == colour
        assert p.array[60][60].colour == colour

    def test_convert_col(self):
        red = [255, 0, 0, 255]
        white = [255, 255, 255, 255]
        black = [0, 0, 0, 255]
        blue = [0, 0, 255, 255]

        e = Editor()

        # TEST 1
        e.create_rgba_array(200, 200, black)
        p = Painter(e.array)
        p.rectangle(p[50][50], p[150][150], white)
        p.convert_col([white], red, True, False, True)

        # Checking colour change worked
        self.assertTrue(p.list_equal(p[55][55].colour, red))
        self.assertTrue(p.list_equal(p[55][145].colour, red))
        self.assertTrue(p.list_equal(p[145][55].colour, red))
        self.assertTrue(p.list_equal(p[145][145].colour, red))

        # Checking invisible_override worked
        self.assertTrue(p[55][55].line)
        self.assertTrue(p[145][55].line)
        self.assertTrue(p[55][145].line)
        self.assertTrue(p[145][145].line)

        # TEST 2
        e.create_rgba_array(200, 200, black)
        p = Painter(e.array)
        p.rectangle(p[50][50], p[150][150], white)
        p.convert_col([white], white, True, True, True)

        # Checking colour change worked
        self.assertTrue(p.list_equal(p[5][5].colour, white))
        self.assertTrue(p.list_equal(p[55][55].colour, white))
        self.assertTrue(p.list_equal(p[145][145].colour, white))
        self.assertTrue(p.list_equal(p[195][195].colour, white))

        # Checking invisible_override worked
        self.assertTrue(p[5][5].line)
        self.assertFalse(p[55][55].line)
        self.assertFalse(p[145][55].line)
        self.assertTrue(p[195][195].line)

        # TEST 3
        # Testing that convert_col to invis can work without changing pixel.colour
        e.create_rgba_array(200, 200, black)
        p = Painter(e.array)
        p.rectangle(p[50][50], p[150][150], white)
        p.convert_col([white], white, False, False, True)

        # Checking colour change did not occur
        self.assertTrue(p.list_equal(p[5][5].colour, black))
        self.assertTrue(p.list_equal(p[55][55].colour, white))
        self.assertTrue(p.list_equal(p[145][145].colour, white))
        self.assertTrue(p.list_equal(p[195][195].colour, black))

        # Checking invisible_override worked
        self.assertFalse(p[5][5].line)
        self.assertTrue(p[55][55].line)
        self.assertTrue(p[145][55].line)
        self.assertFalse(p[195][195].line)

        # TEST 4
        # Testing that convert_col to invis can work off of replacement_colour
        # value without changing colour of pixel.colour
        e.create_rgba_array(200, 200, black)
        p = Painter(e.array)
        p.rectangle(p[50][50], p[150][150], white)
        p.convert_col([white], black, False, True, True)

        # Checking colour change did not occur
        self.assertTrue(p.list_equal(p[5][5].colour, black))
        self.assertTrue(p.list_equal(p[55][55].colour, white))
        self.assertTrue(p.list_equal(p[145][145].colour, white))
        self.assertTrue(p.list_equal(p[195][195].colour, black))

        # Checking invisible_override worked
        self.assertFalse(p[5][5].line)
        self.assertTrue(p[55][55].line)
        self.assertTrue(p[145][55].line)
        self.assertFalse(p[195][195].line)


if __name__ == '__main__':
    unittest.main()
