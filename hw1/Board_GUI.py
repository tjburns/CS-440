import pygame

# This is modified matrix to graphic code sourced from http://programarcadegames.com/python_examples/f.php?file=array_backed_grid.py

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 8
HEIGHT = 8

# This sets the margin between each cell
MARGIN = 1

def board_gui(board):
    
    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    rowT = len(board)
    columnT = len(board[0])
    WINDOW_SIZE = [(WIDTH+MARGIN)*rowT+1, (HEIGHT+MARGIN)*columnT+1]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Maze Traversal")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():    # User did something
            if event.type == pygame.QUIT:   # If user clicked close
                done = True     # Flag that we are done so we exit this loop

        # Set the screen background
        screen.fill(BLACK)

        for row in range(rowT):
            for col in range(columnT):
                color = WHITE
                if board[row][col][0] == 1: # blocked - unseen
                    color = BLACK
                if board[row][col][0] == 2: # blocked - seen
                    color = MAGENTA
                if board[row][col][0] == 3: # target
                    color = GREEN
                if board[row][col][0] == 4: # agent
                    color = BLUE
                if board[row][col][0] == 5: # path
                    color = RED
                if board[row][col][0] == 6: # adaptive path
                    color = YELLOW
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * col + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])


        # Limit to 60 frames per second
        clock.tick(60)
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()