import heapq
import array as arr
import random as ran
import copy
from grid_gen import *
import time

C = 101*101  # highest cost value


# Method to compute an adaptive A* path
def computeAdap(s_state, e_state, maze, gd):

    openList = minHighHeap()
    closedList = []
    curr = s_state
    maze.grid[curr.x][curr.y][1] = maze.getAdaptiveH(gd, curr.g)
    curr.f = maze.grid[curr.x][curr.y][1]
    curr.g = 0

    openList.insert(curr)

    while openList.isEmpty() == False:
        curr = openList.deletemin()
        closedList.append(curr)

        if curr == e_state:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            return path[::-1]

        for co in maze.getNeighbors(curr):
            if co in closedList:
                continue
            if co in openList.heap:
                # Perform update if needed
                newCost = curr.g + 1
                if co.g > newCost:
                    index = openList.heap.index(co)
                    openList.heap[index].g = newCost
                    maze.grid[co.x][co.y][1] = maze.getAdaptiveH(
                        gd, co.g)  # Recalculating new H value
                    # Adjusting the f value of node
                    openList.heap[index].f = newCost + maze.grid[co.x][co.y][1]
                    openList.heap[index].p_node = curr
                    # need to re balance heap potentially
                    openList.siftup(index)
            elif maze.grid[co.x][co.y][0] != 2:  # not blocked and seen
                co.g = curr.g + 1
                # if maze.grid[co.x][co.y][1] == -1:  # not yet visited
                maze.grid[co.x][co.y][1] = maze.getAdaptiveH(gd, co.g)
                co.f = co.g + maze.grid[co.x][co.y][1]
                co.p_node = curr
                openList.insert(co)

    print("No path")
    return None


# Method to compute backwards A* path with built in python heap
def computeBackHeapQ(t_state, s_state, maze):
    openList = []
    closedList = []

    maze.resetH()

    curr = s_state
    maze.grid[curr.x][curr.y][1] = maze.getH(
        curr.x, curr.y, t_state.x, t_state.y)

    curr.f = maze.grid[curr.x][curr.y][1]
    curr.g = 0
    heapq.heappush(openList, curr)

    while len(openList) != 0:
        curr = heapq.heappop(openList)
        closedList.append(curr)

        if curr == t_state:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            return path

        for co in maze.getNeighbors(curr):
            if co in closedList:
                continue
            if co in openList:
                # Perform update if needed
                newCost = curr.g + 1
                if co.g > newCost:
                    co.g = newCost
                    co.f = newCost + maze.grid[co.x][co.y][1]
                    co.p_node = curr
                    # need to re balance heap potentially
                    openList.remove(co)
                    heapq.heappush(openList, co)
            elif maze.grid[co.x][co.y][0] != 2:  # not blocked and seen
                co.g = curr.g + 1
                maze.grid[co.x][co.y][1] = maze.getH(
                    co.x, co.y, t_state.x, t_state.y)
                co.f = co.g + maze.grid[co.x][co.y][1]
                co.p_node = curr
                heapq.heappush(openList, co)

    print("No Path")
    return


# Method to compute a backwards A* path
def computeBacc(t_state, s_state, maze, g_flag):
    if g_flag == 0:
        openList = minLowHeap()
    else:
        openList = minHighHeap()

    closedList = []
    maze.resetH()  # need to reset heuristic on new runs
    curr = s_state
    maze.grid[curr.x][curr.y][1] = maze.getH(
        curr.x, curr.y, t_state.x, t_state.y)
    curr.f = maze.grid[curr.x][curr.y][1]
    curr.g = 0

    openList.insert(curr)

    while openList.isEmpty() == False:
        curr = openList.deletemin()
        closedList.append(curr)

        if curr == t_state:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            return path

        for co in maze.getNeighbors(curr):
            if co in closedList:
                continue
            if co in openList.heap:
                # Perform update if needed
                newCost = curr.g + 1
                if co.g > newCost:
                    index = openList.heap.index(co)
                    openList.heap[index].g = newCost
                    openList.heap[index].f = newCost + maze.grid[co.x][co.y][1]
                    openList.heap[index].p_node = curr
                    # need to re balance heap potentially
                    openList.siftup(index)
            elif maze.grid[co.x][co.y][0] != 2:  # not blocked and seen
                co.g = curr.g + 1
                maze.grid[co.x][co.y][1] = maze.getH(
                    co.x, co.y, t_state.x, t_state.y)
                co.f = co.g + maze.grid[co.x][co.y][1]
                co.p_node = curr
                openList.insert(co)

    print("No Path")
    return


# Method to compute forwards A* path
def computePath(s_state, t_state, maze, g_flag):
    # s_state and t_state are in the format of object coord
    # grid is a Grid object

    # Based on g_flag (which determines whether repeated forward a* prefers
    # low or high g-values if f-values are the same in the heap)
    # we make the open queue

    if g_flag == 1:  # Higher value g-cost
        openList = minHighHeap()
    else:
        openList = minLowHeap()

    closedList = []  # Closed or Travelled List
    curr = coord(s_state.x, s_state.y)  # curr is a coordinate

    # Calculate heuristic/Manhattan distance and insert into grid if not calculated
    if maze.grid[curr.x][curr.y][1] == -1:
        maze.grid[curr.x][curr.y][1] = maze.getH(
            curr.x, curr.y, t_state.x, t_state.y)
    curr.g = 0
    curr.f = maze.grid[curr.x][curr.y][1]
    openList.insert(curr)

    while openList.isEmpty() == False:
        # Find the item with the lowest f(n) cost
        curr = openList.deletemin()
        if curr == t_state:
            path = []
            while curr:
                path.append(curr)
                curr = curr.p_node
            print("Path Found!")

            return path[::-1]

        closedList.append(curr)  # Add curr to closed list

        # Generate all successors and try expanding them
        for co in maze.getNeighbors(curr):
            if co in closedList:
                continue
            if co in openList.heap:
                # check if we need to update it's cost and parent
                new_cost = curr.g + 1
                if(co.g > new_cost):
                    index = openList.heap.index(co)
                    openList.heap[index].g = new_cost
                    openList.heap[index].f = new_cost + \
                        maze.grid[co.x][co.y][1]
                    openList.heap[index].p_node = curr
                    # need to re balance heap potentially
                    openList.siftup(index)
            # assume everything is unblocked to begin with
            elif maze.grid[co.x][co.y][0] != 2:
                # If coordinate isn't in open list, we calculate H and G for the coordinate, each action being 1 to move
                co.g = curr.g + 1
                if maze.grid[co.x][co.y][1] == -1:  # haven't yet encountered this state
                    maze.grid[co.x][co.y][1] = maze.getH(
                        co.x, co.y, t_state.x, t_state.y)

                co.f = co.g + maze.grid[co.x][co.y][1]
                co.p_node = curr
                # Add to open list with the full function value for it's priority

                openList.insert(co)

    print("No path")
    return None

# goal is a coord object of our goal state
# path is a list of coord objects, where the first coord is the starting point
# last coord should always be the goal state
# maze is the currently observed state of the grid by the agent
# We will attempt to move the agent along the path, returns stopping point
# Updates information about blocked neighbors along the way


def moveAgent(goal, path, maze, dir_flag):
    prev = None
    for curr in path:
        if curr == goal:
            print("Path was completed!")
            return goal
        if 1 <= maze.grid[curr.x][curr.y][0] <= 2:
            print("Path was blocked, need to restart A* from parent")
            maze.grid[curr.x][curr.y][0] = 2  # set it to be blocked now
            if dir_flag == 1:  # backwards
                return prev
            return curr.p_node

        for succ in maze.getNeighbors(curr):
            # check to see what neighbors are blocked to update
            if maze.grid[succ.x][succ.y][0] == 1:
                maze.grid[succ.x][succ.y][0] = 2
        # keep track of previous in path in case we need to do backwards
        prev = coord(curr.x, curr.y)
    return  # should not be reached
