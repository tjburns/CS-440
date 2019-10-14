import numpy
from numpy.random import randint as rand
import random as random
import matplotlib.pyplot as pyplot
import pygame
import time

# This is modified matrix to graphic code sourced from http://programarcadegames.com/python_examples/f.php?file=array_backed_grid.py

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 6
HEIGHT = 6

# This sets the margin between each cell
MARGIN = 1


def matrixgraphics(grid):

    # Initialize pygame
    pygame.init()

    # Get the size of the board
    ro = len(grid)
    col = len(grid[0])
    # Set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(
        [(WIDTH+MARGIN)*ro+1, (HEIGHT+MARGIN)*col+1])

    # Set title of screen
    pygame.display.set_caption("GridWorld")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(ro):
            for column in range(col):
                color = WHITE  # clear
                if grid[row][column][0] == 1:  # blocked
                    color = BLUE
                if grid[row][column][0] == 2:  # blocked but seen
                    color = PURPLE
                if grid[row][column][0] == 3:  # target
                    color = GREEN
                if grid[row][column][0] == 4:  # agent
                    color = RED
                if grid[row][column][0] == 5:  # path
                    color = YELLOW
                if grid[row][column][0] == 6:  # adaptive path
                    color = ORANGE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()

