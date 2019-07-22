import unittest
import math
from Editor.Editor import Editor
from Painter import Painter
from Pixel.Pixel import Pixel


class TestPainter(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
