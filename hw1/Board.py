import random

# Defines board that maze is created on.
# Board is a 2d array of Coordinates
class Board:
	def __init__(self, width, height, prob):
		self.width = width
		self.height = height
		self.board = []
		for i in range(self.width):
			self.board.append([])
			if prob >= random.random():
				self.board[i][j].append(1)
			else:
				self.board[i][j].append(0)
			self.board[i][j].append(-1)

	def getCoord(self, x, y):
		if 0 <= x <= self.width and 0 <= y <= self.height:
			return -1
		else:
			return self.board[x][y]

	def getNeighbors(self, coord):
		x = coord.x
		y = coord.y
		neighbors = [Coordinate(x+1, y), Coordinate(x, y-1), Coordinate(x-1, y), Coordinate(x, y+1)]
		if (x+y)%2 == 0:
			neighbors.reverse()
		neighbors = filter(lambda inGrid: 0 <= inGrid.x < self.width and 0 <= inGrid.y < self.height, neighbors)
		return neighbors

	# calculate manhattan distance
	def getHeuristic(self, x1, y1, x2, y2):
		return abs(x1 - x2) + abs(y1 - y2)
	
	def getAdaptiveHeuristic(self, new_g, g):
		return new_g - g
	
	def resetHeuristicVals(self):
        for row in range(self.width):
            for col in range(self.height):
                self.board[row][col][1] = -1
	
# Defines a coordinate for each point on the board.
# Each point contains all information necessary for path traversal algorithms
class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.g = 0
		self.f = 0
		self.p_node = None
	
	# used for comparisons in the MinHighGHeap to maintain order
    def __lt__(self, other):
        if type(self) == type(other):
            if self.f < other.f:
                return True
            elif self.f == other.f:
                return self.g >= other.g
            return False

    # used for comparisons in the MinLowGHeap to maintain order
    def __gt__(self, other):
        if type(self) == type(other):
            if self.f < other.f:
                return True
            elif self.f == other.f:
                return self.g < other.g
            return False

	# used for comparisons in both heaps
    def __eq__(self, other):
        if type(self) == type(other):
            return self.x == other.x and self.y == other.y