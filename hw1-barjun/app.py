from grid_gen import Grid
from grid_gen import coord
from AStar import computePath
from AStar import moveAgent
from AStar import computeBacc
from AStar import computeBackHeapQ
from printGrid import matrixgraphics
import time

starttime = time.time()

myGrid = Grid(101, 101, 0.3)
row = len(myGrid.grid)
col = len(myGrid.grid[0])

# Find first open space near top to place my agent
found = 0
for i in range(row):
    for j in range(col):
        if myGrid.grid[i][j][0] == 0:
            myAgent = coord(i, j)
            found = 1
            break
    if found == 1:
        break

# Find first open space near bottom to place goal
found = 0
x = row-1
while x >= 0:
    y = col-1
    while y >= 0:
        if myGrid.grid[x][y][0] == 0:
            myGoal = coord(x, y)
            found = 1
            break
        y = y - 1
    if found == 1:
        break

myGrid.grid[myAgent.x][myAgent.y][0] = 4
myGrid.grid[myGoal.x][myGoal.y][0] = 3

matrixgraphics(myGrid.grid)
while 1:
    # Forwards version w/ Lower G Value Bias
    path = computePath(myAgent, myGoal, myGrid, 0)

    # Backwards version w/ Lower G Value Bias
    # path = computeBacc(myAgent, myGoal, myGrid, 0)

    # Forwards version w/ Higher G Value Bias
    # path = computePath(myAgent, myGoal, myGrid, 1)

    # Backwards version w/ Higher G Value Bias
    #path = computeBacc(myAgent, myGoal, myGrid, 1)

    # Backwards version w/ Built-in Heap Implementation
    # path = computeBackHeapQ(myAgent, myGoal, myGrid)

    if path == None:
        break

    pathGrid = Grid(101, 101, 0)
    pathGrid.grid[myAgent.x][myAgent.y][0] = 4
    for loc in path:
        pathGrid.grid[loc.x][loc.y][0] = 6
    pathGrid.grid[myGoal.x][myGoal.y][0] = 3
    #matrixgraphics(pathGrid.grid)  # - DONT DELETE, --intermediate grid printing for showing path calculated

    myGrid.grid[myAgent.x][myAgent.y][0] = 4
    xval = myAgent.x
    yval = myAgent.y

    # Forwards Agent Movement
    # myAgent = moveAgent(myGoal, path, myGrid, 0)
    # Backwards Agent Movement
    myAgent = moveAgent(myGoal, path, myGrid, 1)

    myGrid.grid[myAgent.x][myAgent.y][0] = 4

    for co in path:
        if(co == myAgent):
            break
        myGrid.grid[co.x][co.y][0] = 5

    myGrid.grid[xval][yval][0] = 6
    # matrixgraphics(myGrid.grid)  # - DONT DELETE, --intermediate grid printing for showing path travelled

    myAgent.p_node = None  # used to reset the path
    myGoal.p_node = None  # used only for backwards
    if myAgent == myGoal:
        break

endtime = time.time()
runtime = endtime - starttime
print("Runtime in seconds: " + str(runtime))

matrixgraphics(myGrid.grid)
