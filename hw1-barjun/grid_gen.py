import numpy as np
import array as arr
import random as random
import heapq
import time

# UNUSED QUEUE IMPLEMENTATION
"""
class Queue:

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)[1]

    def contains(self, item):
        return item in self.elements

    def update(self, previous, new):
        for x in self.elements:
            if x == previous:
                x = new
                return
"""

class Grid:
    # initialization method
    # Generates any
    # Sets up tuples for each space.  The first number in the tuple represents the blocked state,
    # with the second one representing the heuristic value of that space (initially set to -1)
    # Here are all possible states:
    # 0 = Unblocked
    # 1 = Blocked and unseen
    # 2 = Blocked and seen (can be updated by A* algorithm)
    def __init__(self, width, height, probability):
        self.width = width
        self.height = height
        self.grid = []
        for i in range(self.width):
            self.grid.append([])
            for j in range(self.height):
                self.grid[i].append([])
                if probability >= random.random():
                    self.grid[i][j].append(1)  # blocked and unseen
                else:
                    self.grid[i][j].append(0)  # open
                # append an initial value of -1 for the heuristic
                self.grid[i][j].append(-1)

    def getCoord(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return -1
        else:
            return self.grid[x][y]

    def getNeighbors(self, coordinate):
        x = coordinate.x
        y = coordinate.y
        neighbors = [coord(x+1, y), coord(x, y-1),
                     coord(x-1, y), coord(x, y+1)]
        if(x+y) % 2 == 0:
            neighbors.reverse()
        # Filter will run the lambda function and remove anything from the list that doesn't satisfy the conditions
        # where the coordinate is in the grid
        neighbors = filter(lambda inGrid: 0 <= inGrid.x <
                           self.width and 0 <= inGrid.y < self.height, neighbors)
        return neighbors

    def getH(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1-y2)

    def getAdaptiveH(self, gd, g):
        return gd - g

    def resetH(self):
        for row in range(self.width):
            for col in range(self.height):
                self.grid[row][col][1] = -1

# Defines coordinate on grid
# Holds x, y coordinate
# its parent node
# cost value to get there (based on the state of its grid)
# final cost, which equals h(n) + cost value
# h(n) is stored in grid, not in coordinate


class coord:
    def __init__(self, x, y):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        # self.temp = temp  # wall or not
        self.p_node = None  # parent node
        # self.H = 0  # h(n) value/heuristic value
        self.g = 0  # g(n) value/cost value
        self.f = 0  # f(n) total cost

    # used for the minHighHeap to maintain order
    def __lt__(self, other):
        if type(self) == type(other):
            if self.f < other.f:
                return True
            elif self.f == other.f:
                return self.g >= other.g
            return False

    # used for the minLowHeap to maintain order
    def __gt__(self, other):
        if type(self) == type(other):
            if self.f < other.f:
                return True
            elif self.f == other.f:
                return self.g < other.g
            return False

    def __eq__(self, other):
        if type(self) == type(other):
            return self.x == other.x and self.y == other.y


# Used for Repeated Forward A* that prefers lower g values over higher g
# if they have the same f value
class minLowHeap:
    def __init__(self):
        self.heap = []
        self.heapsize = 0
        self.heap.append(coord(-1, -1))

    # Note: > comparator is weirdly defined above, breaks ties on lower g values
    def siftup(self, i):
        while i // 2 > 0:
            if self.heap[i] > self.heap[i // 2]:
                temp = self.heap[i // 2]
                self.heap[i // 2] = self.heap[i]
                self.heap[i] = temp
            else:
                break
            i = i // 2

    def siftdown(self, i):
        while (i * 2) <= self.heapsize:
            child = self.minchild(i)
            if self.heap[child] > self.heap[i]:
                temp = self.heap[i]
                self.heap[i] = self.heap[child]
                self.heap[child] = temp
            else:
                break
            i = child

    def minchild(self, i):
        if i * 2 + 1 > self.heapsize:
            return i * 2
        else:
            if self.heap[i * 2] > self.heap[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def insert(self, inputcoord):
        self.heap.append(inputcoord)
        self.heapsize = self.heapsize + 1
        self.siftup(self.heapsize)

    def findmin(self):
        return self.heap[1]

    def deletemin(self):
        value = self.heap[1]
        # might need to offset by 1
        self.heap[1] = self.heap[self.heapsize]
        self.heap.pop()
        self.heapsize = self.heapsize - 1
        self.siftdown(1)
        return value

    # Checks if heap is empty
    # The first element is a placeholder so empty state is if there's just one
    def isEmpty(self):
        if len(self.heap) == 1:
            return True
        else:
            return False


# Used for Repeated Forward A* that prefers higher g values over lower g
# if they have the same f value
class minHighHeap:
    def __init__(self):
        self.heap = []
        self.heapsize = 0
        self.heap.append(coord(-1, -1))

    def siftup(self, i):
        # C = 10000  # a constant
        while i // 2 > 0:
            if self.heap[i] < self.heap[i // 2]:
                temp = self.heap[i // 2]
                self.heap[i // 2] = self.heap[i]
                self.heap[i] = temp
            else:
                break
            i = i // 2

    def siftdown(self, i):
        # C = 10000
        while (i * 2) <= self.heapsize:
            child = self.minchild(i)
            if self.heap[child] < self.heap[i]:
                temp = self.heap[i]
                self.heap[i] = self.heap[child]
                self.heap[child] = temp
            else:
                break
            i = child

    def minchild(self, i):
        if i * 2 + 1 > self.heapsize:
            return i * 2
        else:
            if self.heap[i * 2] < self.heap[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def insert(self, inputcoord):
        self.heap.append(inputcoord)
        self.heapsize = self.heapsize + 1
        self.siftup(self.heapsize)

    def findmin(self):
        return self.heap[1]

    def deletemin(self):
        value = self.heap[1]
        self.heap[1] = self.heap[self.heapsize]
        self.heap.pop()
        self.heapsize = self.heapsize - 1
        self.siftdown(1)
        return value

    # Checks if heap is empty
    # The first element is a placeholder so empty state is if there's just one
    def isEmpty(self):
        if len(self.heap) == 1:
            return True
        else:
            return False

