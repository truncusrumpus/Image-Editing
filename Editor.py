from PIL import Image
import numpy as np
import math
import csv
import timeit
import random
from Pixel import Pixel


class Editor:

    def __init__(self, file_name=""):
        self.file_name = file_name
        self.array = None

        if self.file_name != "":
            self.array = self.open_image(self.file_name)

    def open_image(self, file_name):
        test_image = Image.open(file_name)
        image_array = np.array(test_image)
        self.array = image_array
        return image_array

    def file_type(self, file_name):
        """
        Returns the file type for a given file_name.
        Returns False if there is no file type
        """
        string = ""
        check = False
        for i in range(len(file_name) - 1, 0, -1):
            if file_name[i] != ".":
                string = file_name[i] + string
            else:
                check = True
                break
        if check is True and len(string) > 0:
            return string
        return False


    def save_image(self, file_name):
        img = Image.fromarray(self.array)
        img.save(file_name)

    def load_array(self, array):
        self.array = array

    def create_png_array(self, width=500, height=500, colour=[0, 0, 0, 255]):
        png_array = np.zeros([height, width, 4], dtype=np.uint8)
        for h in range(height):
            for w in range(width):
                png_array[h, w] = colour
        self.array = png_array

    def write_array_to_csv(self, file_name, array=None):
        if array is None:
            array = self.array

        with open(file_name, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(array)

        csvFile.close()
        return
