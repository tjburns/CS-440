import math, random

class BoardNode:

    def getIsBlocked(self, p):
        if random.random() >= p:
            return False
        else:
            return True

    def __init__(self, x, y, p, grid):
        self.x = x
        self.y = y
        self.isBlocked = getIsBlocked(p)
        self.isDiscovered = False
        self.next = None

        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.children = []

    def euclidean_distance(self, dest):
        self.distance = math.sqrt(math.pow((self.x - dest.x), 2) + math.pow((self.y - dest.y), 2))
        return self.distance

    def manhattan_distance(self, dest):
        self.distance = math.abs(self.x - dest.x) + math.abs(self.y - dest.y)
        return self.distance
    
    def max_distance(self, dest):
        self.distance = math.pow(math.pow(math.abs(self.x - dest.x), 0.25) + math.pow(math.abs(self.y - dest.y), 0.25), 4)
        return self.distance

    def compare_to(self, n):
        if self.distance < n.distance:
            return -1
        elif self.distance == n.distance:
            return 0
        else:
            return 1

    def compare(self, n1, n2):
        if n1.distance < n2.distance:
            return -1
        elif n1.distance == n2.distance:
            return 0
        else:
            return 1

    def __str__(self):
        return "(" + self.x + ", " + self.y + ")"