from Board import Board, Coordinate
from Min_Heaps import MinHighGHeap, MinLowGHeap

# compute path of foward A*
def forward_a_star(agent_pos, goal_pos, board, g_comparison):

    # check if we are running forward A* tie breaking on high or low g values when f is equal
    if g_comparison == 'high':
        openList = MinHighGHeap()
    elif g_comparison == 'low':
        openList = MinLowGHeap()
    else:
        print("Error forward A* method call.")
        openList = MinHighGHeap()

    closedList = []

    if board.board[agent_pos.x][agent_pos.y][1] == -1:
        board.board[agent_pos.x][agent_pos.y][1] = board.getHeuristic(agent_pos.x, agent_pos.y, goal_pos.x, goal_pos.y)
    agent_pos.g = 0
    agent_pos.f = board.board[agent_pos.x][agent_pos.y][1]

    openList.insert(agent_pos)

    while openList.isEmpty() == False:
        curr = openList.deleteMin()
        if curr == goal_pos:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            print("Path found.")

            return path[::-1]
        
        closedList.append(curr)

        for n in board.getNeighbors(curr):
            if n in closedList:
                continue
            if n in openList.heap:
                cost = curr.g + 1
                if n.g > cost:
                    index = openList.heap.index(n)
                    openList.heap[index].g = cost
                    openList.heap[index].f = cost + board.board[n.x][n.y][1]
                    openList.heap[index].p_node = curr
                    openList.climbUp(index)
            elif board.board[n.x][n.y][0] != 2:
                n.g = curr.g + 1
                if board.board[n.x][n.y][1] == -1:
                    board.board[n.x][n.y][1] = board.getHeuristic(n.x, n.y, goal_pos.x, goal_pos.y)
                n.f = n.g + board.board[n.x][n.y][1]
                n.p_node = curr

                openList.insert(n)
    
    print("No path.")
    return None

# compute path of backward A*
def backward_a_star(agent_pos, goal_pos, board, g_comparison):

    # check if we are running forward A* tie breaking on high or low g values when f is equal
    if g_comparison == 'high':
        openList = MinHighGHeap()
    elif g_comparison == 'low':
        openList = MinLowGHeap()
    else:
        print("Error backward A* method call.")
        openList = MinHighGHeap()

    closedList = []
    
    board.resetHeuristicVals()

    board.board[goal_pos.x][goal_pos.y][1] = board.getHeuristic(goal_pos.x, goal_pos.y, agent_pos.x, agent_pos.y)
    goal_pos.g = 0
    goal_pos.f = board.board[goal_pos.x][goal_pos.y][1]

    openList.insert(goal_pos)

    while openList.isEmpty() == False:
        curr = openList.deleteMin()
        closedList.append(curr)

        if curr == agent_pos:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            return path

        for n in board.getNeighbors(curr):
            if n in closedList:
                continue
            if n in openList.heap:
                cost = curr.g + 1
                if n.g > cost:
                    index = openList.heap.index(n)
                    openList.heap[index].g = cost
                    openList.heap[index].f = cost + board.board[n.x][n.y][1]
                    openList.heap[index].p_node = curr
                    openList.climbUp(index)
            elif board.board[n.x][n.y][0] != 2:
                n.g = curr.g + 1
                board.board[n.x][n.y][1] = board.getHeuristic(n.x, n.y, agent_pos.x, agent_pos.y)
                n.f = n.g + board.board[n.x][n.y][1]
                n.p_node = curr

                openList.insert(n)
    
    print("No path.")
    return None

def adaptive_a_star(agent_pos, goal_pos, board, new_g):
    openList = MinHighGHeap
    closedList = []
    curr = agent_pos
    board.board[curr.x][curr.y][1] = board.getAdaptiveHeuristic(new_g, curr.g)
    curr.f = board.board[curr.x][curr.y][1]
    curr.g = 0

    openList.insert(curr)

    while openList.isEmpty() == False:
        curr = openList.deleteMin()
        closedList.append(curr)

        if curr == goal_pos:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            return path[::-1]

        for n in maze.getNeighbors(curr):
            if n in closedList:
                continue
            if n in openList.heap:
                cost = curr.g+1
                if n.g > cost:
                    index = openList.heap.index(n)
                    openList.heap[index].g = cost
                    board.board[n.x][n.y][1] = board.getAdaptiveHeuristic(new_g, n.g)
                    openList.heap[index].f = cost + board.board[n.x][n.y][1]
                    openList.heap[index].p_node = curr
                    openList.climbUp(index)
            elif board.board[n.x][n.y][0] != 2:
                n.g = curr.g + 1
                board.board[n.x][n.y][1] = board.getAdaptiveHeuristic(new_g, n.g)
                n.g = n.g + board.board[n.x][n.y][1]
                n.p_node = curr
                openList.insert(n)
    
    print("No path.")
    retirm None

# moves the agent along the found path either forwards or backwards
# finds blocked neighbors along path traversal
def agent_traverse(goal_pos, path, board, direction):
    prev = None
    for curr in path:
        if curr == goal:
            print("Path completed.")
            return goal_pos
        # should be 1 or 2 if blocked ((and) seen)
        if 1 <= board.board[curr.x][curr.y][0] <= 2:
            print("Path blocked. Restarting A* from parent.")
            # set as blocked and seen
            board.board[curr.x][curr.y][0] = 2
            if direction = 'backward':
                return prev
            return curr.p_node
        
        # check for blocked neighbors
        for n in board.getNeighbors(curr):
            if board.board[n.x][n.y][0] == 1:
                board.board[n.x, n.y][0] = 2
            
        prev = curr

    print("Error in path traversal.")
    return