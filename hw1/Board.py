from BoardNode import BoardNode

class Board:
	def __init__(self, length, width, p):
		self.grid = [[BoardNode(99,99,p,None) for i in range(length)] for j in range(width)]
		self.length = length
		self.width = width
	
		for i in range(self.length):
			for j in range(self.width):
				n = self.grid[i][j]
				if n.x > 0:
					n.children.append(self.grid[n.x-1][n.y])
				if n.x < self.length-1:
					n.children.append(self.grid[n.x+1][n.y])
				if n.y < self.width-1:
					n.children.append(self.grid[n.x][n.y+1])
				if n.y > 0:
					n.children.append(self.grid[n.x][n.y-1])

		self.src = self.grid[0][0]
		self.dest = self.grid[length-1][width-1]
		self.src.isBlocked = False
		self.dest.isBlocked = False

	def length(self):
		return self.length
	def width(self):
		return self.width

	def print_board(self):
		for i in range(self.length):
			for j in range(self.width):
				if self.grid[i][j] == self.src or self.grid[i][j] == self.dest or self.grid[i][j].isPath:
					print("O", end ='')
				elif self.grid[i][j].isBlocked == False:
					print(" ", end='')
				else:
					print("X", end='')
				
			print()