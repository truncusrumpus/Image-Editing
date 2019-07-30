import unittest
from Editor.Editor import Editor
from Painter.Painter import Painter


class TestPixel(unittest.TestCase):
    def test_adjacent_squares(self):
        e = Editor()
        e.create_rgba_array(200, 200)
        p = Painter(e.array)

        # Testing adjacent squares on top left corner
        adj = p.array[0][0].adjacent_squares(p.array)
        self.assertEqual(adj[0], False)
        self.assertEqual(adj[1], False)
        self.assertNotEqual(adj[2], False)
        self.assertNotEqual(adj[3], False)
        self.assertNotEqual(adj[4], False)
        self.assertEqual(adj[5], False)
        self.assertEqual(adj[6], False)
        self.assertEqual(adj[7], False)

        # Testing adjacent squares on top right corner
        adj = p.array[199][0].adjacent_squares(p.array)
        self.assertEqual(adj[0], False)
        self.assertEqual(adj[1], False)
        self.assertEqual(adj[2], False)
        self.assertEqual(adj[3], False)
        self.assertNotEqual(adj[4], False)
        self.assertNotEqual(adj[5], False)
        self.assertNotEqual(adj[6], False)
        self.assertEqual(adj[7], False)

        # Testing adjacent squares on bottom left corner
        adj = p.array[0][199].adjacent_squares(p.array)
        self.assertNotEqual(adj[0], False)
        self.assertNotEqual(adj[1], False)
        self.assertNotEqual(adj[2], False)
        self.assertEqual(adj[3], False)
        self.assertEqual(adj[4], False)
        self.assertEqual(adj[5], False)
        self.assertEqual(adj[6], False)
        self.assertEqual(adj[7], False)

        # Testing adjacent squares on bottom right corner
        adj = p.array[199][199].adjacent_squares(p.array)
        self.assertNotEqual(adj[0], False)
        self.assertEqual(adj[1], False)
        self.assertEqual(adj[2], False)
        self.assertEqual(adj[3], False)
        self.assertEqual(adj[4], False)
        self.assertEqual(adj[5], False)
        self.assertNotEqual(adj[6], False)
        self.assertNotEqual(adj[7], False)


if __name__ == '__main__':
    unittest.main()