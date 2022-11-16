import numpy as np
from numba import njit
import pygame, time

WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000

BOARD_HEIGHT = 1000
BOARD_WIDTH = 1000

SQUARE_SIZE = WINDOW_HEIGHT // BOARD_HEIGHT

@njit
def Process(board: np.ndarray) -> np.ndarray:
    newBoard = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=np.bool8)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            neighbours = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if k == 0 and l == 0:
                        continue
                    if i + k < 0 or i + k >= BOARD_HEIGHT or j + l < 0 or j + l >= BOARD_WIDTH:
                        continue
                    neighbours += board[i + k, j + l]

                    
            if board[i, j] == 1:                                        # If cell is alive
                if neighbours == 2 or neighbours == 3:                      # If cell has 2 or 3 neighbours
                    newBoard[i, j] = 1                                          # Cell stays alive
            else:                                                       # If cell is dead
                if neighbours == 3:                                         # If cell has 3 neighbours
                    newBoard[i, j] = 1                                          # Cell becomes alive
    return newBoard


board: np.ndarray = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=np.bool8)
# Random cell generation
for i in range(BOARD_HEIGHT):
    for j in range(BOARD_WIDTH):
        if np.random.randint(0, 2) == 1:
            board[i, j] = True

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
loop = True
while (loop) :
    startTime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    board = Process(board)
    window.fill((0, 0, 0))
    
    surf = pygame.surfarray.make_surface(board * 255)
    window.blit(surf, (0, 0))
    pygame.display.flip()
    #display fps
    print(1 / (time.time() - startTime),"fps")