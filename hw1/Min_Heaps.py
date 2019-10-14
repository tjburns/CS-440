# min heap for repeated forward A* when choosing lower g values on tie breaks of equal f values
class MinLowGHeap:
	def __init__(self):
		self.heap = []
		self.heapsize = 0
		self.heap.append(Coordinate(-1,-1))
	
	def insert(self, inputCoord):
		self.heap.append(inputCoord)
		self.heapsize = self.heapsize+1
		self.climbUp(self.heapsize)

	def climbUp(self, i):
		while i//2 > 0:
			if self.heap[i] > self.heap[i//2]:
				temp = self.heap[i//2]
				self.heap[i//2] = self.heap[i]
				self.heap[i] = temp
			else:
				break
			i = i//2
	
	def climbDown(self, i):
		while i*2 <= self.heapsize:
			child = self.minchild(i)
			if self.heap[child] > self.heap[i]:
				temp = self.heap[i]
				self.heap[i] = self.heap[child]
				self.heap[child] = temp
			else:
				break
			i = child
	
	def minChild(self, i):
		if i*2+1 > self.heapsize:
			return i*2
		else:
			if self.heap[i*2] > self.heap[i*2+1]:
				return i*2
			else:
				return i*2+1

	def findMin(self):
		return self.heap[1]

	def deleteMin(self):
		deleteVal = self.findMin()
		self.heap[1] = self.heap[self.heapsize]
		self.heap.pop()
		self.heapsize = self.heapsize-1
		self.climbDown(1)
		return deleteVal

	def isEmpty(self):
		if len(self.heap) == 1:
			return True
		else:
			return False

# min heap for repeated forward A* when choosing higher g values on tie breaks of equal f values
class MinHighGHeap:
	def __init__(self):
		self.heap = []
		self.heapsize = 0
		self.heap.append(Coordinate(-1,-1))

	def insert(self, inputCoord):
		self.heap.append(inputCoord)
		self.heapsize = self.heapsize+1
		self.climbUp(self.heapsize)

	def climbUp(self, i):
		while i//2 > 0:
			if self.heap[i] < self.heap[i//2]:
				temp = self.heap[i//2]
				self.heap[i//2] = self.heap[i]
				self.heap[i] = temp
			else:
				break
			i = i//2
	
	def climbDown(self, i):
		while i*2 <= self.heapsize:
			child = self.minChild(i)
			if self.heap[child] < self.heap[i]:
				temp = self.heap[i]
				self.heap[i] = self.heap[child]
				self.heap[child] = temp
			else:
				break
			i = child
	
	def minChild(self, i):
		if i*2+1 > self.heapsize:
			return i*2
		else:
			if self.heap[i*2] > self.heap[i*2+1]:
				return i*2
			else:
				return i*2+1

	def findMin(self):
		return self.heap[1]

	def deleteMin(self):
		deleteVal = self.findMin()
		self.heap[1] = self.heap[self.heapsize]
		self.heap.pop()
		self.heapsize = self.heapsize-1
		self.climbDown(1)
		return deleteVal

	def isEmpty(self):
		if len(self.heap) == 1:
			return True
		else:
			return False