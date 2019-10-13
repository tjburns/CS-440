from Board import Board
from BoardNode import BoardNode

if __name__ == '__main__':
    length = 100
    width = 100
    p = 0.3

    maze = Board(length,width, p)
    maze.print_board()