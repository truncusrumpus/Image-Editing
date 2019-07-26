class Pixel:
    def __init__(self, x, y, colour=None):
        self.x = x
        self.y = y
        self.colour = colour
        self.line = False

    def adjacent_squares(self, array):
        """
        Returns an array of the Pixels adjacent to self.
        [Up, Upper Right, Right, Lower Right, Down, Lower Left, Left, Upper Left]
        If an adjacent pixel is outside the boundaries of the array, returns False
        """

        width = len(array)
        height = len(array[0])

        assert 0 <= self.x < width and 0 <= self.y < height, "x: " + str(self.x) + ", y: " + str(self.y)

        # UP
        if 0 <= (self.y - 1) < height:
            up = array[self.x][self.y - 1]
        else:
            up = False

        # UP - RIGHT
        if 0 <= (self.y - 1) < height and 0 <= (self.x + 1) < width:
            up_right = array[self.x + 1][self.y - 1]
        else:
            up_right = False

        # RIGHT
        if 0 <= (self.x + 1) < width:
            right = array[self.x + 1][self.y]
        else:
            right = False

        # DOWN - RIGHT
        if 0 <= (self.y + 1) < height and 0 <= (self.x + 1) < width:
            down_right = array[self.x + 1][self.y + 1]
        else:
            down_right = False

        # DOWN
        if 0 <= (self.y + 1) < height:
            down = array[self.x][self.y + 1]
        else:
            down = False

        # DOWN - LEFT
        if 0 <= (self.y + 1) < height and 0 <= (self.x - 1) < width:
            down_left = array[self.x - 1][self.y + 1]

        else:
            down_left = False

        # LEFT
        if 0 <= (self.x - 1) < width:
            left = array[self.x - 1][self.y]
        else:
            left = False

        # UP - LEFT
        if 0 <= (self.y - 1) < height and 0 <= (self.x - 1) < width:
            up_left = array[self.x - 1][self.y - 1]
        else:
            up_left = False

        return [up, up_right, right, down_right, down, down_left, left, up_left]

    def adjacent_squares_unconditional(self, array):
        """
        Returns an array of the cells adjacent to self.
        [Up, Upper Right, Right, Lower Right, Down, Lower Left, Left, Upper Left]
        If no adjacent cell exists in 'array', then returns a Pixel instance
        with property, Pixel.colour = False
        """

        width = len(array)
        height = len(array[0])

        # UP
        if 0 <= (self.y - 1) < height and 0 <= self.x < width:
            up = array[self.x][self.y - 1]
        else:
            up = Pixel(self.x, self.y - 1, False)

        # UP - RIGHT
        if 0 <= (self.y - 1) < height and 0 <= (self.x + 1) < width:
            up_right = array[self.x + 1][self.y - 1]
        else:
            up_right = Pixel(self.x + 1, self.y - 1, False)

        # RIGHT
        if 0 <= self.y < height and 0 <= (self.x + 1) < width:
            right = array[self.x + 1][self.y]
        else:
            right = Pixel(self.x + 1, self.y, False)

        # DOWN - RIGHT
        if 0 <= (self.y + 1) < height and 0 <= (self.x + 1) < width:
            down_right = array[self.x + 1][self.y + 1]
        else:
            down_right = Pixel(self.x + 1, self.y + 1, False)

        # DOWN
        if 0 <= (self.y + 1) < height and 0 <= self.x < width:
            down = array[self.x][self.y + 1]
        else:
            down = Pixel(self.x, self.y + 1, False)

        # DOWN - LEFT
        if 0 <= (self.y + 1) < height and 0 <= (self.x - 1) < width:
            down_left = array[self.x - 1][self.y + 1]
        else:
            down_left = Pixel(self.x - 1, self.y + 1, False)

        # LEFT
        if 0 <= self.y < height and 0 <= (self.x - 1) < width:
            left = array[self.x - 1][self.y]
        else:
            left = Pixel(self.x - 1, self.y, False)

        # UP - LEFT
        if 0 <= (self.y - 1) < height and 0 <= (self.x - 1) < width:
            up_left = array[self.x - 1][self.y - 1]
        else:
            up_left = Pixel(self.x - 1, self.y - 1, False)

        return [up, up_right, right, down_right, down, down_left, left, up_left]
