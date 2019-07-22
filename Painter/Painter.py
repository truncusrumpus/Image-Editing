from PIL import Image
import numpy as np
import math
import timeit
import time
import random
from Package.Fill_Queue import FillQueue
from Pixel.Pixel import Pixel


class Painter:
    def __init__(self, array, filename=""):
        self.width = len(array[0])
        self.height = len(array)
        self.array = self.format_array(array)
        self.filename = filename

    def format_array(self, array):
        """
        Transposes an array and makes each cell an instance of Pixel(x_coord, y_coord, colour)
        """
        formatted_array = [[None for _ in range(self.height)] for _ in range(self.width)]
        for w in range(self.width):
            for h in range(self.height):
                formatted_array[w][h] = Pixel(w, h, array[h][w])
        return formatted_array

    def export_array(self):
        """
        Returns a transposed array of self.array with each pixel converted into
        an array depicting [r, g, b, a] values. Main purpose is to prepare
        painter.array to be converted into an image
        """
        export_array = np.zeros([self.height, self.width, 4], dtype=np.uint8)
        for w in range(self.width):
            for h in range(self.height):
                export_array[h, w] = self.array[w][h].colour
        return export_array

    def list_equal(self, array1, array2):
        """Returns True if two lists are equal. Returns False otherwise"""
        if len(array1) != len(array2):
            return False
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True

    def dist_2d(self, x1, y1, x2, y2):
        """
        Returns the distance (float) from (x1, y1) to (x2, y2)
        """
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    def straight_line(self, start, end, colour=[0, 0, 0, 255], stroke_weight=1):
        """
        Draws a straight line from the start pixel to the end pixel
        Eg: start = (10, 10), end = (100, 100), line = top left : bottom right
        Eg: start = (100, 100), end = (10, 10), line =  bottom right : top left
        Eg: start = (10, 100), end = (100, 10), line = bottom left : top right
        Eg: start = (100, 10), end = (10, 100), line = top right : bottom left

        :param start: Start Pixel
        :param end: End Pixel
        :param colour: [r, g, b, a]
        :param stroke_weight: int >= 1
        """

        assert type(start.x) is int and type(start.y) is int, "Coord's are not int's"
        assert type(end.x) is int and type(end.y) is int, "Coord's are not int's"

        # Gradient = Undefined (vertical line)
        if start.x == end.x:
            if 0 <= start.x < self.width:
                for y in range(start.y, end.y + 1):
                    if 0 <= y < self.height:
                        self.circle_fill(self.array[start.x][y], int(stroke_weight + 0.5), colour)
            return end

        # Gradient = 0 (horizontal line)
        elif start.y == end.y:
            if 0 <= start.y < self.height:
                for x in range(start.x, end.x + 1):
                    if 0 <= x < self.width:
                        self.circle_fill(self.array[x][start.y], int(stroke_weight + 0.5), colour)
            return end

        # Initialising while loop
        x_count = start.x
        y_count = start.y
        if 0 <= x_count < self.width and 0 <= y_count < self.height:
            self.array[x_count][y_count].colour = colour

        m = (end.y - start.y) / (end.x - start.x)  # m = gradient
        m_down = math.floor(m)
        m_up = math.ceil(m)
        m_round = round(m)
        m_inv = 1/m
        m_inv_round = round(1 / m)
        m_inv_down = math.floor(1 / m)
        m_inv_up = math.ceil(1 / m)

        iterate_x = True
        if m < -1 or m > 1:
            iterate_x = False

        change = 0
        if iterate_x:
            if start.x < end.x:
                change = 1
            elif start.x > end.x:
                change = -1
            x_count += change
            y_count += m_round * change
        else:
            if start.y < end.y:
                change = 1
            elif start.y > end.y:
                change = -1
            y_count += change
            x_count += m_inv_round * change

        if 0 <= x_count < self.width and 0 <= y_count < self.height:
            self.array[x_count][y_count].colour = colour

        while True:
            if x_count != start.x:
                current_m = (y_count - start.y) / (x_count - start.x)
            else:
                current_m = 0

            if iterate_x:
                x_count += change

                # If grad at current pixel is less than gradient at end
                # pixel, then add the gradient at end pixel rounded up
                if abs(current_m) < abs(m):
                    if abs(m) == m:
                        y_count += m_up * change
                    else:
                        y_count += m_down * change

                # If grad at current pixel is more than gradient at end
                # pixel, then add the gradient at end pixel rounded down
                elif abs(current_m) > abs(m):
                    if abs(m) == m:
                        y_count += m_down * change
                    else:
                        y_count += m_up * change

                # If grad at current pixel is equal to gradient at end
                # pixel, then add the gradient at end pixel rounded normally
                elif abs(current_m) == abs(m):
                    y_count += m_round * change
            else:
                if current_m != 0:
                    current_m_inv = 1 / current_m
                else:
                    current_m_inv = 0
                y_count += change

                # If grad at current pixel is less than gradient at end
                # pixel, then add the gradient at end pixel rounded up
                if abs(current_m_inv) < abs(m_inv):
                    if abs(m) == m:
                        x_count += m_inv_up * change
                    else:
                        x_count += m_inv_down * change

                # If grad at current pixel is more than gradient at end
                # pixel, then add the gradient at end pixel rounded down
                elif abs(current_m_inv) > abs(m_inv):
                    if abs(m) == m:
                        x_count += m_inv_down * change
                    else:
                        x_count += m_inv_up * change

                # If grad at current pixel is equal to gradient at end
                # pixel, then add the gradient at end pixel rounded normally
                elif abs(current_m_inv) == abs(m_inv):
                    x_count += m_inv_round * change

            # Will draw a circle of radius equal to stroke_weight
            if 0 <= x_count < self.width and 0 <= y_count < self.height:
                self.circle_fill(self.array[x_count][y_count], int(stroke_weight + 0.5), colour)

            if y_count == end.y and x_count == end.x:
                break

        return end

    def circle_fill(self, centre, radius=1, colour=[0, 0, 0, 255]):
        """
        Draws a circle of colour, 'colour', with radius, 'radius', at pixel, 'centre'

        :param centre: Pixel(int, int)
        :param radius: int >= 0
        :param colour: [r, g, b, a]
        :return:
        """
        assert type(centre.x) is int and type(centre.y) is int, "Coord's are not int's"
        assert radius >= 0
        for ink in colour:
            assert 0 <= ink <= 255

        for x in range(centre.x - radius + 1, centre.x + radius):
            for y in range(centre.y - radius + 1, centre.y + radius):
                if 0 <= x < self.width and 0 <= y < self.height:
                    if not self.list_equal(self.array[x][y].colour, colour):
                        if self.dist_2d(centre.x, centre.y, x, y) <= radius:
                            self.array[x][y].colour = colour

        return centre

