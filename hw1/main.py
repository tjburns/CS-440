from Board import Board, Coordinate
from Min_Heaps import MinHighGHeap, MinLowGHeap
from Board_GUI import board_gui 
from a_star import forward_a_star, backward_a_star, adaptive_a_star, agent_traverse
import time

"""
Value on Board : State of Coordinate : Color
--------------------------------------------
1 : # blocked - unseen   : BLACK
2 : # blocked - seen     : BLUE
3 : # target             : GREEN
4 : # agent              : RED
5 : # path               : MAGENTA
6 : # adaptive path      : YELLOW
"""

startTime = time.time()

test_maze = Board(101, 101, 0.3)
row = len(test_maze.board)
col = len(test_maze.board[0])

# place agent in the first unblocked position in the top-leftmost coordinate on the board
found = 0
for i in range(row):
    for j in range(col):
        if test_maze.board[i][j][0] == 0:
            test_agent = Coordinate(i, j)
            found = 1
            break
    if found == 1:
        break

test_maze.board[test_agent.x][test_agent.y][0] = 4

# place goal in the first unblocked position in the bottom-rightmost coordinate on the board
found = 0
for i in range(row-1, -1, -1):
    for j in range(col-1, -1. -1):
        if test_maze.board[i][j][0] == 0:
            test_goal = Coordinate(i, j)
            found = 1
            break
    if found == 1:
        break

test_maze[test_goal.x][test_goal.y][0] = 3

board_gui(test_maze.board)

while True:

    # Forward A* - Lower G
    #path = forward_a_star(test_agent, test_goal, test_maze, 'low')
    # Backward A* - Lower G
    #path = backward_a_star(test_agent, test_goal, test_maze, 'low')

    # Forward A* - Higher G
    path = forward_a_star(test_agent, test_goal, test_maze, 'high')
    # Backward A* - Higher G
    #path = backward_a_star(test_agent, test_goal, test_maze, 'high')

    # Adaptive A* - High G
    #path = adaptive_a_star(test_agent, test_goal, test_maze, 0)

    if path == None:
        break

    path_board = Board(101,101,0)
    path_board.board[test_agent.x][test_agent.y][0] = 4
    for coord in path:
        path_board.board[coord.x][coord.y][0] = 6
    path_board.board[test_goal.x][test_goal.y][0] = 3

    # PRINT INTERMEDIATE PATH CALCULATIONS
    board_gui(path_board.board)

    test_maze.board[test_agent.x][test_agent.y][0] = 4
    xval = test_agent.x
    yval = test_agent.y 

    # FORWARD AGENT TRAVERSAL
    test_agent = agent_traverse(test_goal, path, test_maze, 'forward')
    # BACKWARD AGENT TRAVERSAL
    #test_agent = agent_traverse(test_goal, path, test_maze, 'backward')

    test_maze.board[test_agent.x][test_agent.y][0] = 4

    for coord in path:
        if coord == test_agent:
            break
        test_maze.board[coord.x][coord.y][0] = 5

    # PRINT INTERMEDIATE PATH TRAVERSAL
    board_gui(test_maze.board)

    test_agent.p_node = None
    test_goal.p_node = None
    if test_agent == test_goal:
        break
    
board_gui(board.grid)

endTime = time.time()
totalTime = endTime - startTime
print("Total Runtime: " + str(totalTime))