class Board:
	def _init_(self, length, width, p):
		self.grid = [[' ' for i in range(10)] for j in range(10)]
		self.length = length
		self.width = width
	
	visited = []
	for i in range(length):
		for j in range(width):
			if (