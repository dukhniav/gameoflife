import pygame
import sys
from random import randint
import numpy as np

#Init
pygame.init()
clock = pygame.time.Clock()

# Params
WINX = 500
WINY = 500
CELLSIZE = 10
HEIGHT = int(WINX/CELLSIZE)
WIDTH = int(WINY/CELLSIZE)
FPS = 5
GENERATION = 1
TEMP_CELLS = np.zeros((HEIGHT, WIDTH), dtype=np.int)
CELLS = np.zeros((WIDTH, HEIGHT), dtype=np.int)

# Game status
DONE = False

# Colors
BLACK = (0, 0, 0)
GREY = (30, 30, 30)
WHITE = (255, 255, 255)


# Set up
print("Set up", end="", flush=True)
screen = pygame.display.set_mode((WINX, WINY))
pygame.display.set_caption("Game of Life")
screen.fill(WHITE)
print("...done")


# Generate world with random alive/dead units throughout the map
print("Generating world", end="", flush=True)
for x in range(WIDTH):
    for y in range(HEIGHT):
        # 0 = DEAD
        # 1 = ALIVE
        CELLS[x][y] = randint(0, 1)
print("...done")


# Find neightbors in surrounding area
def findNeighbors(grid, x, y):
    if 0 < x < len(grid) - 1:
        xi = (0, -1, 1)
    elif x > 0:
        xi = (0, -1)
    else:
        xi = (0, 1)

    if 0 < y < len(grid[0]) - 1:
        yi = (0, -1, 1)
    elif y > 0:
        yi = (0, -1)
    else:
        yi = (0, 1)

    for a in xi:
        for b in yi:
            if a == b == 0:
                continue
            yield grid[x + a][y + b]


def update(grid, x, y):
    # determine num of living neighbors for this cell
    neighbors = findNeighbors(CELLS, x, y)
    alive = 0
    for i in neighbors:
        if i == 1:
            alive += 1

    # if current cell is alive
    if grid[x][y] == 1:
        # kill if less than 2 or more than 3 alive neighbors
        if (alive < 2) or (alive > 3):
            return 0
        else:
            return 1
    # if current cell is dead
    elif grid[x][y] == 0:
        # make alive if 3 alive neighbors
        if alive == 3:
            return 1
        else:
            return 0



def main():
    global DONE

    while not DONE:
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                DONE = True

        # update cells
        for x in range(0, WIDTH):
            for y in range(0, HEIGHT):
                CELLS[x][y] = update(TEMP_CELLS, x, y)
            pygame.display.flip()

        # draw grid
        for j in range(0, WINX, CELLSIZE):
            for k in range(0, WINY, CELLSIZE):
                # if cell is alive
                if CELLS[int(j/CELLSIZE)][int(k/CELLSIZE)] == 1:
                    # draw red square
                    pygame.draw.rect(screen, BLACK, [j, k, CELLSIZE, CELLSIZE])
                else:
                    # draw black square
                    pygame.draw.rect(screen, WHITE, [j, k, CELLSIZE, CELLSIZE])
                # draw square border
                pygame.draw.rect(screen, GREY, [j, k, CELLSIZE, CELLSIZE], 1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if CELLS[int(Mouse_x/CELLSIZE)][int(Mouse_y/CELLSIZE)] == 0:
                CELLS[int(Mouse_x/CELLSIZE)][int(Mouse_y/CELLSIZE)] = 1



        # draw updates
        pygame.display.update()

        # generations per second
        clock.tick(FPS)


if __name__ == '__main__':
    main()