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
        string = ""
        for i in range(len(file_name) - 1, 0):
            if file_name[i] != ".":
                string += file_name[i]
            else:
                return string

    def save_image(self, file_name):
        img = Image.fromarray(self.array)
        img.save(file_name)

    def load_array(self, array):
        self.array = array

    def modify_rgb_array(self, r=False, g=False, b=False, a=False):
        """Modifies every pixel in self.array to have the input r, g, b & a values"""
        if self.file_name == "":
            raise FileExistsError("A file has not yet been read")

        for array in self.array:
            for pixel in array:
                self.modify_pixel_rgb(pixel, r, g, b, a)

        return

    def modify_pixel_rgb(self, pixel, r=False, g=False, b=False, a=False):
        """Modifies a pixel to have the input r, g, b & a values"""

        if r is not False:
            pixel[0] = r
        if g is not False:
            pixel[1] = g
        if b is not False:
            pixel[2] = b
        if a is not False:
            pixel[3] = a

        return

    def pixelate(self, p_width, p_height):
        if self.file_name == "":
            raise FileExistsError("A file has not yet been read")

        if p_width < 1 and p_height < 1:
            raise ValueError("The pixelation height or width is invalid")

        array_width = len(self.array)
        array_height = len(self.array[0])
        [pixel_w, pixel_h] = self.calc_pixelate_div(array_width, array_height, p_width, p_height)

        for w in range(0, len(self.array), pixel_w):
            for h in range(0, len(self.array[w]), pixel_h):
                [r, g, b, a] = self.calc_pixels_avg(w, h, pixel_w, pixel_h)
                for inner_w in range(pixel_w):
                    for inner_h in range(pixel_h):
                        if h+inner_h >= len(self.array[0]) or w+inner_w >= len(self.array):
                            continue
                        # If .png colour pixel:
                        if self.array[w+inner_w][h+inner_h].size == 4:
                            self.modify_pixel_rgb(self.array[w+inner_w][h+inner_h], r, g, b, a)
                        # If .jpg colour pixel:
                        if self.array[w + inner_w][h + inner_h].size == 3:
                            self.modify_pixel_rgb(self.array[w + inner_w][h + inner_h], r, g, b)
                        # If .png grey scale pixel
                        elif self.array[w+inner_w][h+inner_h].size == 1:
                            self.array[w + inner_w][h + inner_h] = a

        return

    def calc_pixelate_div(self, t_width, t_height, i_width, i_height, error=0.5):
        """
        Calculates the best possible values (total width % pixelation width == 0, etc)
        for the pixelation width and height within the error margin
        """
        if t_width % i_width != 0:
            # If the error margin would include values below 1
            r_min = int((1 - error) * i_width)
            if r_min < 1:
                r_min = 1

            # Searching for factors of total width within the error margin
            w_result = 0
            for w in range(r_min, int((1+error)*i_width)):
                # If this pixel width is a factor of the total width:
                if t_width % w == 0:
                    # If this factor is closer than a previous factor to desired width
                    if abs(i_width - w) < abs(i_width - w_result):
                        w_result = w
            # If a factor could not be found in error margin, use desired value with remainder
            if w_result == 0:
                w_result = i_width
        else:
            w_result = i_width

        if t_height % i_height != 0:
            # If the error margin would include values below 1
            r_min = int((1 - error) * i_height)
            if r_min < 1:
                r_min = 1

            h_result = 0
            for h in range(r_min, int((1+error) * i_height)):
                # If this pixel width is a factor of the total width:
                if t_height % h == 0:
                    # If this factor is closer than a previous factor to desired height
                    if abs(i_height - h) < abs(i_height - h_result):
                        h_result = h
            # If a factor could not be found in error margin, use desired value with remainder
            if h_result == 0:
                h_result = i_height
        else:
            h_result = i_height

        return [w_result, h_result]

    def calc_pixels_avg(self, x_co, y_co, x_num, y_num):
        """Finds the average rgb and a values of the pixels from
        [x_co, x_co + x_num] and [y_co, y_co + y_num] in self.array"""
        r_avg = -0.01
        g_avg = -0.01
        b_avg = -0.01
        a_avg = -0.01

        max_x = x_co + x_num
        if max_x >= len(self.array):
            max_x = len(self.array) - 1
        max_y = y_co + y_num
        if max_y >= len(self.array[0]):
            max_y = len(self.array[0]) - 1
        for x in range(x_co, max_x):
            for y in range(y_co, max_y):
                # print(str(x) + ", " + str(y))
                if self.array[x][y].size == 1:
                    a_avg += self.array[x][y]
                elif self.array[x][y].size == 4:
                    r_avg += self.array[x][y][0]
                    g_avg += self.array[x][y][1]
                    b_avg += self.array[x][y][2]
                    a_avg += self.array[x][y][3]
                elif self.array[x][y].size == 3:
                    r_avg += self.array[x][y][0]
                    g_avg += self.array[x][y][1]
                    b_avg += self.array[x][y][2]

        if r_avg == -0.01 and g_avg == -0.01 and b_avg == -0.01:
            r_avg = g_avg = b_avg = a_avg

        if a_avg == -0.01:
            a_avg = 240

        num = x_num*y_num
        r_avg = int(r_avg / num + 0.5)
        g_avg = int(g_avg / num + 0.5)
        b_avg = int(b_avg / num + 0.5)
        a_avg = int(a_avg / num + 0.5)

        return [r_avg, g_avg, b_avg, a_avg]

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
