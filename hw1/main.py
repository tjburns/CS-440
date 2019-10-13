from Board import Board
from BoardNode import BoardNode

if __name__ == '__main__':
    length = 20
    width = 20
    p = 0.3

    maze = Board(length,width, p)
    maze.print_board()