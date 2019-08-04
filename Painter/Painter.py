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

    def __getitem__(self, index):
        return self.array[index]

    def __setitem__(self, key, item):
        self.array[key] = item

    def format_array(self, array):
        """
        Transposes an array and makes each cell an instance of Pixel(x_coord, y_coord, colour)
        """
        formatted_array = [[None for _ in range(self.height)] for _ in range(self.width)]
        for w in range(self.width):
            for h in range(self.height):
                if len(array[h][w]) == 4:
                    formatted_array[w][h] = Pixel(w, h, array[h][w])
                elif len(array[h][w]) == 3:
                    col = [array[h][w][0]] + [array[h][w][1]] + [array[h][w][2]] + [255]
                    formatted_array[w][h] = Pixel(w, h, col)
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
                export_array[h, w] = self[w][h].colour
        return export_array

    def invert_rgba_image_col(self):
        for w in range(self.width):
            for h in range(self.height):
                col = self.inverse_rgb_colour(self[w][h].colour)
                self[w][h].colour = col

    def inverse_rgb_colour(self, colour):
        inverse_colour = [None]*4
        inverse_colour[0] = 255 - colour[0]
        inverse_colour[1] = 255 - colour[1]
        inverse_colour[2] = 255 - colour[2]
        inverse_colour[3] = colour[3]
        return inverse_colour

    def interpolate_pixel(self, cell, ip_index):
        diff_pixels = 0
        adj_coloured_count = 0
        adj = cell.adjacent_squares(self.array)

        # Counting how many of the adjacent pixels are coloured and actually exist
        for p in adj:
            if p is not False:
                if p.colour is not False:
                    if not self.list_almost_equal(p.colour, [0, 0, 0, 255], 30):
                        diff_pixels += 1
                    adj_coloured_count += 1

        # Only interpolating pixels where the proportion of 'different' pixels is greater than
        # the ip_index given (eg: for ip_index = 0.8, 4/5 or more pixels must be 'different'
        if diff_pixels/adj_coloured_count < ip_index:
            return

        # Applying the weighting given by the user (ip_index) to the
        new_col = [None] * (len(cell.colour) - 1)
        for c in range(len(new_col)):
            new_col[c] = round(ip_index * cell.colour[c], 8)

        # Calculating weightings for each of the adjacent pixels' colours
        adj_ip_index = round(abs(1 - ip_index) / adj_coloured_count, 8)

        for p in adj:
            if p is not False:
                if p.colour is not False:
                    for c in range(len(p.colour) - 1):
                        new_col[c] += p.colour[c] * adj_ip_index

        for c in range(len(new_col) - 1):
            if new_col[c] >= 253.5:
                new_col[c] = int(new_col[c] + 0.5)
            else:
                new_col[c] = int(new_col[c] + 2.5)

        new_col.append(255)
        self[cell.x][cell.y].colour = new_col

    def interpolate(self, interpolate_index):
        for w in range(self.width):
            for h in range(self.height):
                self.interpolate_pixel(self[w][h], interpolate_index)
                if self.width >= 100:
                    if w % int(0.01 * self.width + 0.5) == 0:
                        print("\rLoading: {:.0f}%".format(w / self.width * 100), end='')
            if w % int(0.25 * self.width + 0.5) == 0:
                if self.filename != "":
                    img = Image.fromarray(self.export_array())
                    img.save(self.filename)

        print("\rInterpolate Complete.")

    def convert_col_to_invisible(self, colour, replacement_colour=None, override=False):
        for w in range(self.width):
            for h in range(self.height):
                if not override:    # override = False (default)
                    if self.list_equal(self[w][h].colour, colour):
                        if replacement_colour is not None:
                            self[w][h].colour = replacement_colour
                        self[w][h].line = True
                else:   # override = True
                    if replacement_colour is not None:
                        # if self[w][h].colour != replacement_colour:
                        if not self.list_almost_equal(self[w][h].colour, replacement_colour, 20):
                            self[w][h].colour = replacement_colour
                            self[w][h].line = True

    def pixel_equal(self, pixel1, pixel2):
        if pixel1.x != pixel2.x or pixel1.y != pixel2.y:
            return False
        if pixel1.colour is False or pixel2.colour is False:
            if pixel1.colour != pixel2.colour:
                return False
        else:
            if not self.list_equal(pixel1.colour, pixel2.colour):
                return False
        if pixel1.line != pixel2.line:
            return False

        return True

    def copy_pixel(self, input_pixel):
        pixel = Pixel(input_pixel.x, input_pixel.y, input_pixel.colour)
        pixel.line = input_pixel.line
        return pixel

    def list_equal(self, array1, array2):
        """Returns True if two lists are equal. Returns False otherwise"""
        if array1 is False or array2 is False:
            return False
        if len(array1) != len(array2):
            return False
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True

    def list_almost_equal(self, array1, array2, error):
        """Returns True if two lists are almost equal. Meaning, if the difference in
        each element's value in the two lists is less than error, returns True.
        Returns False otherwise"""
        if len(array1) != len(array2):
            return False
        for i in range(len(array1)):
            if abs(array1[i] - array2[i]) > error:
                return False
        return True

    def list_avg(self, array):
        """Returns the average value of a list"""
        return round(round(sum(array), 10) / len(array), 10)

    def list_diff_avg(self, array):
        """Returns the average of all of the differences between
        adjacent elements in the list
        eg: list = [1, 2, 4, 7], list_diffs = [1, 2, 3], list_diff_avg = 2"""
        if len(array) == 1:
            return 0

        diff_sum = 0
        for i in range(1, len(array)):
            diff_sum += array[i] - array[i-1]
        return diff_sum / (len(array) - 1)

    def dist_2d(self, x1, y1, x2, y2):
        """
        Returns the distance (float) from (x1, y1) to (x2, y2)
        """
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    def suitable_centre_end(self, start):
        w = int(self.width / 4 + 0.5)
        h = int(self.height / 4 + 0.5)

        # TOO LEFT
        if start.x < self.width / 2:
            # TOO HIGH
            if start.y < self.height / 2:
                centre_end = Pixel(random.randint(start.x, self.width + w), random.randint(start.y, self.height + h))
            # TOO LOW
            else:
                centre_end = Pixel(random.randint(start.x, self.width + w), random.randint(-h, start.y))
        # TOO RIGHT
        elif start.x > self.width / 2:
            # TOO HIGH
            if start.y < self.height / 2:
                centre_end = Pixel(random.randint(-w, start.x), random.randint(start.y, self.height + h))
            # TOO LOW
            else:
                centre_end = Pixel(random.randint(-w, start.x), random.randint(-h, start.y))
        else:
            centre_end = Pixel(random.randint(-w, self.width + w), random.randint(-h, self.height + h))

        return centre_end

    def straight_line(self, start, end, colour=[0, 0, 0, 255], stroke_weight=1, controlled=False):
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

        if start.line is True:
            return start

        prev = start

        # Gradient = Undefined (vertical line)
        if start.x == end.x:
            if 0 <= start.x < self.width:
                for y in range(start.y, end.y + 1):
                    if 0 <= y < self.height:
                        if controlled is True:
                            if self[start.x][y].line is True:
                                return prev
                            prev = self[start.x][y]
                        else:
                            self[start.x][y].line = True
                        if stroke_weight >= 0.5:
                            self.circle_fill(self[start.x][y], int(stroke_weight + 0.5), colour)

            return end

        # Gradient = 0 (horizontal line)
        elif start.y == end.y:
            if 0 <= start.y < self.height:
                for x in range(start.x, end.x + 1):
                    if 0 <= x < self.width:
                        if controlled is True:
                            if self[x][start.y].line is True:
                                return prev
                            prev = self[x][start.y]
                        else:
                            self[x][start.y].line = True
                        if stroke_weight >= 0.5:
                            self.circle_fill(self[x][start.y], int(stroke_weight + 0.5), colour)
            return end

        # Initialising while loop
        x_count = start.x
        y_count = start.y
        if 0 <= x_count < self.width and 0 <= y_count < self.height:
            if controlled is True:
                if self[x_count][y_count].line is True:
                    return prev
                prev = self[x_count][y_count]
            else:
                self[x_count][y_count].line = True
            if stroke_weight >= 0.5:
                self[x_count][y_count].colour = colour

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
            if controlled is True:
                if self[x_count][y_count].line is True:
                    return prev
                prev = self[x_count][y_count]
            else:
                self[x_count][y_count].line = True
            if stroke_weight >= 0.5:
                self[x_count][y_count].colour = colour

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
                if controlled is True:
                    if self[x_count][y_count].line is True:
                        return prev
                    prev = self[x_count][y_count]
                else:
                    self[x_count][y_count].line = True
                if stroke_weight >= 0.5:
                    self.circle_fill(self[x_count][y_count], int(stroke_weight + 0.5), colour)

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
                    if not self.list_equal(self[x][y].colour, colour):
                        if self.dist_2d(centre.x, centre.y, x, y) <= radius:
                            if self[x][y].line is not True:
                                self[x][y].colour = colour

        return centre

    def paint_drop_line(self, start, end, colour=[0, 0, 0, 255], stroke=(1, 1)):
        assert type(start.x) is int and type(start.y) is int, "Coord's are not int's"
        assert type(end.x) is int and type(end.y) is int, "Coord's are not int's"

        stroke_weight = stroke[0]
        dist = self.dist_2d(start.x, start.y, end.x, end.y)
        stroke_iter = (stroke[1]-stroke[0])/dist

        # Gradient = Undefined (vertical line)
        if start.x == end.x:
            if 0 <= start.x < self.width:
                for y in range(start.y, end.y + 1):
                    if 0 <= y < self.height:
                        self.circle_fill(self.array[start.x][y], int(stroke_weight + 0.5), colour)
                    stroke_weight += stroke_iter

            return end

        # Gradient = 0 (horizontal line)
        elif start.y == end.y:
            if 0 <= start.y < self.height:
                for x in range(start.x, end.x + 1):
                    if 0 <= x < self.width:
                        self.circle_fill(self.array[x][start.y], int(stroke_weight + 0.5), colour)
                    stroke_weight += stroke_iter
            return end

        # Initialising while loop
        x_count = start.x
        y_count = start.y
        if 0 <= x_count < self.width and 0 <= y_count < self.height:
            self.array[x_count][y_count].colour = colour
            stroke_weight += stroke_iter

        m = (end.y - start.y) / (end.x - start.x)  # m = gradient
        m_down = math.floor(m)
        m_up = math.ceil(m)
        m_round = round(m)
        m_inv = 1 / m
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
            stroke_weight += stroke_iter

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
                stroke_weight += stroke_iter

            if y_count == end.y and x_count == end.x:
                break

        return end

    def old_curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1):
        """
        Draws a proportion of a circle (curve) from start Pixel with a centre Pixel.

        :param start: The start position of the curve, Pixel(x, y, colour)
        :param centre: The centre position of the curve, Pixel(x, y, colour)
        :param proportion: The proportion of the circle to be drawn, [0, 1]
        :param colour: The colour of the curve to be drawn, [r, g, b, a]
        :param stroke_weight: The stroke weight of the curve, [0, infinity]
        :return: The end position of the curve
        """

        # radius:
        r = self.dist_2d(start.x, start.y, centre.x, centre.y)
        # circumference:
        circ = math.pi*2*r

        if r == 0:
            return

        # Initialising colour drawing
        if start.colour is not False:
            if stroke_weight >= 0.5:
                self.circle_fill(start, round(stroke_weight), colour)
            if start.colour is not False:
                self[start.x][start.y].line = True
        current = start

        # Trigonometric calculations variables
        # Used to measure whether angle is increasing (first half) or
        # decreasing (second half) for each 360 degree rotation:
        angle_diff_avg = False
        prev_angles = []
        # Used to compare current distance to previous distances in
        # order to rig distances for pixels that could cause errors:
        prev_dist = []
        # A counter for the while loop, measures the proportion completed so far:
        arc_proportion = 0
        # Each iteration represents 180 degrees completed so far:
        iterations = 0

        # Calculating a suitable length for prev_angles
        prev_angles_len = int(math.pi*r/36 + 0.5)       # 1/40 of circumference
        if prev_angles_len < 10:                        # or, if required:
            prev_angles_len = int(math.pi*r/3 + 0.5)    # 1/6 of circumference

        # Could pick first adjacent square here to choose which way curve goes
        prev = None  # The previous Pixel, used to make sure don't go backwards

        # A backup counter that iterates for each Pixel, checked against the
        # estimated number of pixels that should be iteration through, with error margin:
        backup_count = 0

        # While loop iterates around the circle until the proportion iterated through
        # so far is equal to the proportion desired or if that doesn't work,
        # the backup counter becomes greater than the estimated number of pixel iterations
        while arc_proportion < proportion and backup_count < circ + 5:

            # Finding next Pixel
            adj = current.adjacent_squares_unconditional(self.array)

            # Initializing Comparison Checks for finding next pixel
            min_diff = 20000        # Initialising with arbitrary large value
            chosen_cell = None

            # Iterating through adjacent Pixel to find one closest to circumference line
            # of curve that is also not the previous or current Pixel
            for cell in adj:
                if cell:
                    dist = self.dist_2d(cell.x, cell.y, centre.x, centre.y)
                    dist = abs(r - dist)
                    if dist < min_diff:
                        if prev is not None:
                            if cell.x == prev.x and cell.y == prev.y:
                                continue
                        min_diff = dist
                        chosen_cell = cell

            prev = current
            current = chosen_cell

            # FOR TESTING!!!
            # Seeing when a Pixel has already been assigned the colour
            try:
                if all(current.colour == colour):
                    pass
                    # point where circle rejoins itself
            except TypeError:
                pass

            # Setting colour of current square and adjacents (if desired)
            if current.colour is not False:
                if stroke_weight >= 0.5:
                    self.circle_fill(current, round(stroke_weight), colour)
                self[current.x][current.y].line = True

            # Distance calculations
            dist = self.dist_2d(current.x, current.y, start.x, start.y)
            if dist > 2*r:                   # Distance between two pixels is greater than
                dist = 2*r                   # diameter which is not possible for calculations

            # Decreasing angle - grad(angle) = negative
            if len(prev_dist) > 1:
                if angle_diff_avg < 0:
                    if dist > self.list_avg(prev_dist):
                        dist = 1.25*prev_dist[len(prev_dist) - 1] - 0.25*prev_dist[len(prev_dist) - 2]
                # Increasing angle - grad(angle) = positive
                elif angle_diff_avg > 0:
                    if dist < self.list_avg(prev_dist):
                        dist = 1.25*prev_dist[len(prev_dist) - 1] - 0.25*prev_dist[len(prev_dist) - 2]

            if dist > 2*r:                   # Distance between two pixels is greater than
                dist = 2*r

            if len(prev_dist) > 2:
                prev_dist.pop(0)
            if angle_diff_avg != 0:
                prev_dist.append(dist)

            # Angle calculations
            alpha = math.acos(dist/(2*r))
            angle = math.pi - 2*alpha

            # Trigonometric Calculations
            if angle_diff_avg is not False:
                if len(prev_angles) > prev_angles_len:
                    prev_angles.pop(0)
                prev_angles.append(angle)
                # Using an average value for prev_angle to assure comparisons are correct
                angle_diff_avg = self.list_diff_avg(prev_angles)
            else:
                if len(prev_angles) > prev_angles_len:
                    prev_angles.pop(0)
                prev_angles.append(angle)
                angle_diff_avg = self.list_diff_avg(prev_angles)

            if angle == math.pi:
                prev_angles = []
                prev_dist = []
                angle_diff_avg = 0

            # Checks for adding to iterations
            if angle_diff_avg is not False:
                # If grad(angle) is negative (second half)
                if angle_diff_avg < 0 and iterations % 2 == 0:
                    iterations += 1
                # If grad(angle) is positive (first half)
                elif angle_diff_avg > 0 and iterations % 2 == 1:
                    iterations += 1

            # Total angle if end position is in 3rd or 4th quadrant
            if iterations % 2 == 1:
                arc_proportion = ((iterations + 1)*math.pi - angle)/(2*math.pi)
            # Total angle if end position is in 1st or 2nd quadrant
            elif iterations % 2 == 0:
                arc_proportion = (angle + iterations * math.pi) / (2 * math.pi)

            # TESTING PURPOSES!!!
            # print("x: " + str(current.x) + ", y: " + str(current.y))
            # if round(arc_proportion, 4) * 1000 % 4 == 0 or arc_proportion > 0.9:
            # if arc_proportion == 1:
            #     print("prop: {0:1.4f}, backup_count: {1:2}, circ: {2:4.4f}".format(arc_proportion, backup_count, circ))
            # test_diff = 10000
            # test_omega = 1
            # if arc_proportion > 0.95:
            #     for i in range(1, int(r + 0.5)):
            #         if abs(arc_proportion - (backup_count + i)/circ) < test_diff:
            #             test_diff = abs(arc_proportion - (backup_count + i)/circ)
            #             test_omega = i
            #     print("test_diff: {0:1.4f}, test_omega: {1}".format(test_diff, test_omega))
            # # print("diff = {0:1.4}".format(arc_proportion - backup_count/circ))
            # img = Image.fromarray(self.export_array())
            # img.save("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

            backup_count += 1

            # END OF WHILE LOOP

        # Testing purposes
        if proportion == 1:
            assert current.x == start.x and current.y == start.y, "(" + str(current.x) + ", " + str(current.y) + ")"
        # print("r: " + str(r) + ", circ: " + str(2*math.pi*r) + ", Count: " + str(backup_count))

        return current

    def curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1, controlled=False):
        """
        Draws a proportion of a circle (curve) from start Pixel with a centre Pixel.

        :param start: The start position of the curve, Pixel(x, y, colour)
        :param centre: The centre position of the curve, Pixel(x, y, colour)
        :param proportion: The proportion of the circle to be drawn, [0, 1]
        :param colour: The colour of the curve to be drawn, [r, g, b, a]
        :param stroke_weight: The stroke weight of the curve, [0, infinity]
        :return: The end position of the curve
        """

        # radius:
        r = self.dist_2d(start.x, start.y, centre.x, centre.y)
        if r == 0:
            return
        # circumference:
        circ = math.pi*2*r

        # Initialising colour drawing
        if start.colour is not False:
            if stroke_weight >= 0.5:
                self.circle_fill(start, round(stroke_weight), colour)
            self[start.x][start.y].line = True
        current = start

        # Trigonometric calculations variables
        # A counter for the while loop, measures the proportion completed so far:
        arc_proportion = 0
        backup_count = 0
        omega = 0.732219602 + 0.627778635 * r
        end_backup_count = round(circ - omega)
        alpha = 1
        alpha_iter = (omega - 1)/end_backup_count

        # Could pick first adjacent square here to choose which way curve goes
        prev = None  # The previous Pixel, used to make sure don't go backwards

        # While loop iterates around the circle until the proportion iterated through
        # so far is equal to the proportion desired or if that doesn't work,
        # the backup counter becomes greater than the estimated number of pixel iterations
        while arc_proportion < proportion and backup_count < circ + 5:

            # Finding next Pixel
            adj = current.adjacent_squares_unconditional(self.array)

            # Initializing Comparison Checks for finding next pixel
            min_diff = 20000        # Initialising with arbitrary large value
            chosen_cell = None

            # Iterating through adjacent Pixel to find one closest to circumference line
            # of curve that is also not the previous or current Pixel
            for cell in adj:
                if cell:
                    dist = self.dist_2d(cell.x, cell.y, centre.x, centre.y)
                    dist = abs(r - dist)
                    if dist < min_diff:
                        if prev is not None:
                            if cell.x == prev.x and cell.y == prev.y:
                                continue
                        min_diff = dist
                        chosen_cell = cell

            prev = current
            current = chosen_cell

            # Setting colour of current square and those adjacent (if desired)
            if current.colour is not False:
                if controlled is True:
                    if current.line is True:
                        return current
                if stroke_weight >= 0.5:
                    self.circle_fill(current, round(stroke_weight), colour)
                self[current.x][current.y].line = True

            # TESTING PURPOSES!!!
            # print("x: " + str(current.x) + ", y: " + str(current.y))
            # img = Image.fromarray(self.export_array())
            # img.save("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

            alpha += alpha_iter
            arc_proportion = (backup_count + alpha)/circ

            backup_count += 1

            # END OF WHILE LOOP

        return current

    def paint_drop_curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=(1, 1)):
        """
        Draws a proportion of a circle (curve) from start Pixel with a centre Pixel.

        :param start: The start position of the curve, Pixel(x, y, colour)
        :param centre: The centre position of the curve, Pixel(x, y, colour)
        :param proportion: The proportion of the circle to be drawn, [0, 1]
        :param colour: The colour of the curve to be drawn, [r, g, b, a]
        :param stroke: A tuple = (start_stroke_weight, end_stroke_weight)
        :return: The end position of the curve
        """

        # radius:
        r = self.dist_2d(start.x, start.y, centre.x, centre.y)
        if r == 0:
            return
        # circumference:
        circ = math.pi*2*r

        stroke = stroke_weight[0]

        # Initialising colour drawing
        if start.colour is not False:
            if stroke >= 0.5:
                self.circle_fill(start, round(stroke), colour)
            self[start.x][start.y].line = True
        current = start

        # Trigonometric calculations variables
        # A counter for the while loop, measures the proportion completed so far:
        arc_proportion = 0
        backup_count = 0
        omega = 0.732219602 + 0.627778635 * r
        end_backup_count = round(circ - omega)
        alpha = 1
        alpha_iter = (omega - 1)/end_backup_count

        stroke_iter = (stroke_weight[1] - stroke_weight[0]) / end_backup_count

        # Could pick first adjacent square here to choose which way curve goes
        prev = None  # The previous Pixel, used to make sure don't go backwards

        # While loop iterates around the circle until the proportion iterated through
        # so far is equal to the proportion desired or if that doesn't work,
        # the backup counter becomes greater than the estimated number of pixel iterations
        while arc_proportion < proportion and backup_count < circ + 5:

            # Finding next Pixel
            adj = current.adjacent_squares_unconditional(self.array)

            # Initializing Comparison Checks for finding next pixel
            min_diff = 20000        # Initialising with arbitrary large value
            chosen_cell = None

            # Iterating through adjacent Pixel to find one closest to circumference line
            # of curve that is also not the previous or current Pixel
            for cell in adj:
                if cell:
                    dist = self.dist_2d(cell.x, cell.y, centre.x, centre.y)
                    dist = abs(r - dist)
                    if dist < min_diff:
                        if prev is not None:
                            if cell.x == prev.x and cell.y == prev.y:
                                continue
                        min_diff = dist
                        chosen_cell = cell

            prev = current
            current = chosen_cell

            # Setting colour of current square and those adjacent (if desired)
            if current.colour is not False:
                if stroke >= 0.5:
                    self.circle_fill(current, round(stroke), colour)
                self[current.x][current.y].line = True

            # TESTING PURPOSES!!!
            # print("x: " + str(current.x) + ", y: " + str(current.y))
            # img = Image.fromarray(self.export_array())
            # img.save("C:/Users/hughr/Downloads/Images/Image Editing/test_output.png")

            alpha += alpha_iter
            arc_proportion = (backup_count + alpha)/circ

            backup_count += 1
            stroke += stroke_iter

            # END OF WHILE LOOP

        return current

    def paint_fill(self, start, fill_colour, background_colour):
        """
        Iterates over an area, deemed to be background_colour, setting colour of Pixels
        to be fill_colour until it reaches a Pixel of a different colour or one that is part
        of an invisible line (used for filling shapes without the need for a border)

        :param start: Pixel to begin paint filling
        :param fill_colour: The colour to fill area with
        :param background_colour: The designated back colour for the area to be filled
        :return:
        """

        # If pixel is not in painter array, return
        if start.colour is False:
            return start

        # If pixel is not the 'background colour', return
        if not self.list_equal(start.colour, background_colour):
            return start

        if start.line is True:
            return start

        # Start pixel colour = designated 'fill colour'
        start.colour = fill_colour

        # Creating queue (FIFO)
        queue = FillQueue()

        # Adding start pixel to end of queue
        queue.append(start)

        # While queue is not empty
        while not queue.is_empty():
            # Removing first node (pixel) from queue
            pixel = queue.serve()

            adj = pixel.adjacent_squares(self.array)

            # If the color of pixel to left of n is background_colour set
            # color of pixel to fill_colour and add pixel to the end of queue
            if adj[6]:
                if self.list_equal(adj[6].colour, background_colour):
                    if adj[6].line is False:
                        adj[6].colour = fill_colour
                        queue.append(adj[6])

            # If the color of pixel to right of n is background_colour set
            # color of pixel to fill_colour and add pixel to the end of queue
            if adj[2]:
                if self.list_equal(adj[2].colour, background_colour):
                    if adj[2].line is False:
                        adj[2].colour = fill_colour
                        queue.append(adj[2])

            # If the color of pixel above n is background_colour set
            # color of pixel to fill_colour and add pixel to the end of queue
            if adj[0]:
                if self.list_equal(adj[0].colour, background_colour):
                    if adj[0].line is False:
                        adj[0].colour = fill_colour
                        queue.append(adj[0])

            # If the color of pixel below n is background_colour set
            # color of pixel to fill_colour and add pixel to the end of queue
            if adj[4]:
                if self.list_equal(adj[4].colour, background_colour):
                    if adj[4].line is False:
                        adj[4].colour = fill_colour
                        queue.append(adj[4])

        # If queue is empty, return
        return start

    def paint_fill_canvas_skip(self, colours, background_colour, skip=(1, 1), timeout=600):
        """
        Iterates over the painter canvas with x iter value = skip[0] and y iter value = skip[1]
        calling paint_fill on the coords
        :param colours: An array of colours from which a colour is randomly chosen for each paint_fill
        :param background_colour: The designated background_colour for each paint_fill call
        :param skip: A tuple = (x_iter_value, y_iter_value)
        :param timeout: The amount of time designated by the user before the function times out
        :return:
        """

        start_time = timeit.default_timer()
        random.seed()
        for w in range(0, self.width, skip[0]):
            for h in range(0, self.height, skip[1]):
                if self.list_equal(self.array[w][h].colour, background_colour):
                    colour = colours[random.randint(0, len(colours) - 1)]
                    self.paint_fill(self.array[w][h], colour, background_colour)
                    if timeit.default_timer() - start_time > 600:
                        break

            print("\rLoading: {:.0f}%".format(w / self.width * 100), end='')
            if w % int(self.width/2) == 0:
                if self.filename != "":
                    img = Image.fromarray(self.export_array())
                    img.save(self.filename)

        if self.filename != "":
            img = Image.fromarray(self.export_array())
            img.save(self.filename)
        print("\rPaint Fill Render Complete.")

    def grid(self, row_num, column_num, colour, stroke_weight):
        grid_width = self.width - stroke_weight
        grid_height = self.height - stroke_weight

        # Drawing column lines
        for x in range(0, grid_width, round(grid_width / column_num)):
            start = self[x][0]
            end = self[x][self.height - 1]
            self.straight_line(start, end, colour, stroke_weight)

        start = self[self.width - 1][0]
        end = self[self.width - 1][grid_height - 1]
        self.straight_line(start, end, colour, stroke_weight)

        # Drawing row lines
        for y in range(0, grid_height, round(grid_height / row_num)):
            start = self[0][y]
            end = self[grid_width - 1][y]
            self.straight_line(start, end, colour, stroke_weight)

        start = self[0][self.height - 1]
        end = self[self.width - 1][self.height - 1]
        self.straight_line(start, end, colour, stroke_weight)

    def artist5(self, num_shapes=10, stroke_range=(1, 100),
                colours=None, timeout=600, pf=[None, 1], image_updating=False):
        """
        Includes paint_fill - paint_fill runs num_shapes times post-order with other methods

        :param num_shapes:
        :param stroke_range:
        :param colours:
        :param timeout:
        :param pf = [paint_fill_background_colour, paint_fill_proportion]
        :param image_updating: Controls whether the actual image is updated on each iteration
        :return:
        """

        random.seed()  # initializer for random methods
        time_start = timeit.default_timer()  # initializer for timeout function

        funcs = [self.straight_line, self.circle_fill, self.curve_centre,
                 self.paint_drop_line, self.paint_drop_curve_centre, self.paint_fill]
        start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
        orig_start = start
        stroke = random.randint(stroke_range[0], stroke_range[1])
        orig_stroke = stroke
        paint_fill_counter = 0

        for i in range(num_shapes):
            colour = colours[random.randint(0, len(colours) - 1)]
            func = funcs[random.randint(0, len(funcs) - 1)]

            centre_end = self.suitable_centre_end(start)

            # [self.straight_line, self.circle_fill, self.curve_centre, self.paint_drop_line, self.paint_fill]
            # straight_line(self, start, end, colour=[0, 0, 0, 255], stroke_weight=1)
            if func == self.straight_line:
                start = func(start, centre_end, colour, stroke)

            # circle_fill(self, centre, radius=1, colour=[0, 0, 0, 255], stroke=[0, 0, 0, 255])
            elif func == self.circle_fill:
                start = func(start, random.randint(stroke, stroke_range[1]), colour)

            # curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1)
            elif func == self.curve_centre:
                proportion = random.randint(100, 900) / 1000
                start = func(start, centre_end, proportion, colour, stroke)

            # paint_drop_curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=(1, 1))
            elif func == self.paint_drop_curve_centre:
                stroke_end = random.randint(stroke_range[0], stroke_range[1])
                proportion = random.randint(100, 900) / 1000
                start = func(start, centre_end, proportion, colour, (stroke, stroke_end))
                stroke = stroke_end

            # paint_drop_line(self, start, end, colour=[0, 0, 0, 255], stroke=(1, 1))
            elif func == self.paint_drop_line:
                stroke_end = random.randint(stroke_range[0], stroke_range[1])
                start = func(start, centre_end, colour, (stroke, stroke_end))
                stroke = stroke_end

            # paint_fill(self, start, fill_colour, background_colour)
            elif func == self.paint_fill:
                paint_fill_counter += 1

            # Timeout function
            if timeit.default_timer() - time_start > timeout:
                break

            # TESTING PURPOSES ONLY!!!
            # img = Image.fromarray(self.export_array())
            # img.save("test_output.png")

            if num_shapes >= 1000:
                image_update_index = 100
            elif num_shapes >= 10:
                image_update_index = 10
            else:
                image_update_index = num_shapes

            if i % int(num_shapes / image_update_index + 0.5) == 0:
                if image_updating:
                    if self.filename != "":
                        img = Image.fromarray(self.export_array())
                        img.save(self.filename)
                print("\rLoading: {:.0f}%".format(i / num_shapes * 100), end='')

        self.paint_drop_line(start, orig_start, colour, (stroke, orig_stroke))

        if self.filename != "":
            img = Image.fromarray(self.export_array())
            img.save(self.filename)

        for i in range(int(num_shapes*pf[1])):
            print("\rLoading: {:.0f}%".format(i / (num_shapes*pf[1]) * 100), end='')
            start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            colour = colours[random.randint(0, len(colours) - 1)]
            if pf[0] is None:
                self.paint_fill(start, colour, start.colour)
            else:
                self.paint_fill(start, colour, pf[0])
            if i % num_shapes == 0 or i % int(num_shapes/2) == 0:
                img = Image.fromarray(self.export_array())
                img.save(self.filename)

        print("\rRender Complete.")


        return

    def artist6(self, num_shapes=10, stroke_weight=1, colours=None, replace_colour=None, timeout=600):

        print("Loading...", end='')
        # Storing pixels with invisible line to be restored later
        invis_queue = FillQueue()
        for w in range(self.width):
            for h in range(self.height):
                if self[w][h].line is True:
                    invis_queue.append(self.copy_pixel(self[w][h]))

        random.seed()  # initializer for random methods
        time_start = timeit.default_timer()  # initializer for timeout function

        # funcs = [self.straight_line, self.curve_centre]
        funcs = [self.straight_line]

        start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
        orig_start = start

        for i in range(num_shapes):
            colour = colours[random.randint(0, len(colours) - 1)]
            func = funcs[random.randint(0, len(funcs) - 1)]

            centre_end = self.suitable_centre_end(start)

            # straight_line(self, start, end, colour=[0, 0, 0, 255], stroke_weight=1)
            if func == self.straight_line:
                start = func(start, centre_end, colour, stroke_weight)

            # curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1)
            elif func == self.curve_centre:
                proportion = random.randint(100, 900) / 1000
                start = func(start, centre_end, proportion, colour, stroke_weight)

            # Timeout function
            if timeit.default_timer() - time_start > timeout:
                break

            if num_shapes >= 1000:
                image_update_index = 100
            elif num_shapes >= 10:
                image_update_index = 10
            else:
                image_update_index = num_shapes

            if i % int(num_shapes / image_update_index + 0.5) == 0:
                print("\rLoading: {:.0f}%".format(i / num_shapes * 100), end='')

            if i % int(0.25 * num_shapes + 0.5) == 0:
                if self.filename != "":
                    img = Image.fromarray(self.export_array())
                    img.save(self.filename)

        self.straight_line(start, orig_start, colour, stroke_weight)

        while not invis_queue.is_empty():
            pixel = invis_queue.serve()
            if replace_colour is not None:
                self[pixel.x][pixel.y].colour = replace_colour
            else:
                self[pixel.x][pixel.y].colour = pixel.colour
            self[pixel.x][pixel.y].line = pixel.line

        if self.filename != "":
            img = Image.fromarray(self.export_array())
            img.save(self.filename)

        print("\rRender Complete.")


        return

    def artist7(self, num_shapes=10, stroke_weight=1, colours=None, timeout=600):

        print("Loading...", end='')

        random.seed()  # initializer for random methods
        time_start = timeit.default_timer()  # initializer for timeout function

        # funcs = [self.straight_line, self.curve_centre]
        funcs = [self.straight_line]

        start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
        while start.line is True:
            start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]

        prev_start = start

        for i in range(num_shapes):
            colour = colours[random.randint(0, len(colours) - 1)]
            func = funcs[random.randint(0, len(funcs) - 1)]

            centre_end = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
            # centre_end = self.suitable_centre_end(start)
            # print("start: {0} , c_end: {1}".format(start, centre_end))

            # straight_line(self, start, end, colour=[0, 0, 0, 255], stroke_weight=1)
            if func == self.straight_line:
                start = func(start, centre_end, colour, stroke_weight, True)

            # curve_centre(self, start, centre, proportion=0.25, colour=[0, 0, 0, 255], stroke_weight=1)
            elif func == self.curve_centre:
                proportion = random.randint(100, 900) / 1000
                start = func(start, centre_end, proportion, colour, stroke_weight)

            # If the function is getting caught in a position it cannot move from, start from somewhere else
            if self.pixel_equal(start, prev_start):
                start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
                while start.line is True:
                    start = self.array[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]

            prev_start = start

            # Timeout function
            if timeit.default_timer() - time_start > timeout:
                break

            if num_shapes >= 1000:
                image_update_index = 100
            elif num_shapes >= 10:
                image_update_index = 10
            else:
                image_update_index = num_shapes

            if i % int(num_shapes / image_update_index + 0.5) == 0:
                print("\rLoading: {:.0f}%".format(i / num_shapes * 100), end='')

            if i % int(0.25 * num_shapes + 0.5) == 0:
                if self.filename != "":
                    img = Image.fromarray(self.export_array())
                    img.save(self.filename)

        if self.filename != "":
            img = Image.fromarray(self.export_array())
            img.save(self.filename)

        print("\rRender Complete.")

        return
