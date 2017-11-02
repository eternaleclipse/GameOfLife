import time
import sys
import pygame

BOARD_WIDTH = 80
BOARD_HEIGHT = 80
BORDER_SIZE = 1
CELL_SIZE = 10
DEAD_COLOR = (100, 0, 0)
LIVE_COLOR = (255, 0, 0)
UPDATE_INTERVAL = 0.05

WINDOW_WIDTH = BOARD_WIDTH * (CELL_SIZE + BORDER_SIZE)
WINDOW_HEIGHT = BOARD_HEIGHT * (CELL_SIZE + BORDER_SIZE)

# Glider
board = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
]

# Glider gun
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Fill missing rows
for i in xrange(BOARD_HEIGHT - len(board)):
    board += [[0] * BOARD_WIDTH]

# Fill missing columns
for y in xrange(len(board)):
    board[y] = board[y] + [0] * (BOARD_WIDTH - len(board[y]))

def print_board():
    for y in xrange(BOARD_HEIGHT):
        for x in xrange(BOARD_WIDTH):
            if board[y][x] == 1:
                print "X",
            else:
                print ".",
        print

def draw_board(window):
    x, y = 0, 0

    step = CELL_SIZE + BORDER_SIZE
    for x in xrange(0, BOARD_WIDTH):
        for y in xrange(0, BOARD_HEIGHT):
            if board[y][x] == 1:
                color = LIVE_COLOR
            else:
                color = DEAD_COLOR
            pygame.draw.rect(window, color, (x * (CELL_SIZE + BORDER_SIZE), y * (CELL_SIZE + BORDER_SIZE), CELL_SIZE, CELL_SIZE))

def neighbor_count(x, y):
    count = 0
    
    for n_y in xrange(y - 1, y + 2):
        for n_x in xrange(x - 1, x + 2):
            n_x, n_y = n_x % BOARD_WIDTH, n_y % BOARD_HEIGHT
            
            if n_x < 0:
                n_x += width
                
            if n_y < 0:
                n_y += height
            
            if board[n_y][n_x] == 1 and (x, y) != (n_x, n_y):
                count += 1
                
    return count
    
def cell_step(x, y):
    is_alive = bool(board[y][x])
    count = neighbor_count(x, y)
    
    if count == 3 or (is_alive and count == 2):
        return True

    return False
        
def step():
    new_board = [[0] * BOARD_WIDTH for line in xrange(BOARD_HEIGHT)]
    
    for y in xrange(BOARD_HEIGHT):
        for x in xrange(BOARD_WIDTH):
            new_board[y][x] = int(cell_step(x, y))
    
    return new_board

def main():
    global board
    pygame.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Game of Life')

    while True:
        draw_board(window)
        time.sleep(UPDATE_INTERVAL)
        board = step()
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

if __name__ == "__main__":
    main()