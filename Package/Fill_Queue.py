class Node:
    def __init__(self, item=None, link=None):
        self.item = item
        self.link = link


class FillQueue:
    def __init__(self):
        """Builds a queue with given capacity > 0"""
        self.count = 0
        self.front = None
        self.rear = None

    def size(self):
        """Returns the size of the stack"""
        return self.count

    def is_empty(self):
        return self.count == 0

    @staticmethod
    def is_full(self):
        return False

    def append(self, item):
        """Places the given item at the end of the queue
        if there is capacity, or raises an exception"""
        new_node = Node(item)
        assert self.count >= 0, "self.count is not positive"

        if self.count > 0:
            # Making current rear node link to new node
            self.rear.link = new_node
            # Making current rear node the new node
            self.rear = self.rear.link
        elif self.count == 0:
            self.front = new_node
            self.rear = new_node

        self.count += 1

    def serve(self):            # Serve = move front += 1
        """Removes and returns the first element of the queue,
        or raises an Exception if there is none.
        Resets the array if it is empty"""
        if self.is_empty():
            raise ValueError("The queue is empty")

        assert self.front is not None, "self.front is None"
        assert self.count >= 0, "self.count is not positive"

        item = self.front.item
        self.front.item = None
        self.front = self.front.link
        self.count -= 1

        return item