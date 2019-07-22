import unittest
from Editor.Editor import Editor
from Painter.Painter import Painter
from Pixel import Pixel


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


if __name__ == '__main__':
    unittest.main()