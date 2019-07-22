import unittest
from Editor import Editor


class TestEditor(unittest.TestCase):
    def test_file_type(self):
        e = Editor()
        # Testing file_type works for all file types
        self.assertEqual(e.file_type("test.py"), "py")
        self.assertEqual(e.file_type("test.jpg"), "jpg")
        self.assertEqual(e.file_type("test.txt"), "txt")
        self.assertEqual(e.file_type("test.mpeg"), "mpeg")
        self.assertEqual(e.file_type("test.mp4"), "mp4")
        
        # Testing file_type returns False for no file type
        self.assertEqual(e.file_type("test"), False)
        self.assertEqual(e.file_type("test."), False)


if __name__ == '__main__':
    unittest.main()