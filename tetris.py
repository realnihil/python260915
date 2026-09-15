import random
import pygame

WIDTH, HEIGHT = 300, 600
CELL = 30
COLS, ROWS = 10, 20
BLACK = (15, 15, 15)
GRAY = (45, 45, 45)
COLORS = [
    (0, 240, 240), (0, 0, 240), (240, 160, 0),
    (240, 240, 0), (0, 240, 0), (160, 0, 240), (240, 0, 0)
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def valid(board, shape, x, y):
    for row, line in enumerate(shape):
        for col, cell in enumerate(line):
            if cell:
                px, py = x + col, y + row
                if px < 0 or px >= COLS or py >= ROWS:
                    return False
                if py >= 0 and board[py][px]:
                    return False
    return True


def merge(board, shape, x, y, color):
    for row, line in enumerate(shape):
        for col, cell in enumerate(line):
            if cell and y + row >= 0:
                board[y + row][x + col] = color


def clear_lines(board):
    remaining = [row for row in board if any(cell == 0 for cell in row)]
    cleared = ROWS - len(remaining)
    return [[0] * COLS for _ in range(cleared)] + remaining, cleared


def draw(screen, board, shape, x, y, color):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            value = board[row][col]
            rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if value:
                pygame.draw.rect(screen, COLORS[value - 1], rect.inflate(-2, -2))

    for row, line in enumerate(shape):
        for col, cell in enumerate(line):
            if cell and y + row >= 0:
                rect = pygame.Rect((x + col) * CELL, (y + row) * CELL, CELL, CELL)
                pygame.draw.rect(screen, color, rect.inflate(-2, -2))

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    board = [[0] * COLS for _ in range(ROWS)]
    shape = random.choice(SHAPES)
    color = random.randrange(1, 8)
    x, y = 3, -len(shape)
    fall_timer = 0
    running = True

    while running:
        elapsed = clock.tick(60)
        fall_timer += elapsed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid(board, shape, x - 1, y):
                    x -= 1
                elif event.key == pygame.K_RIGHT and valid(board, shape, x + 1, y):
                    x += 1
                elif event.key == pygame.K_DOWN and valid(board, shape, x, y + 1):
                    y += 1
                elif event.key == pygame.K_UP:
                    rotated = rotate(shape)
                    if valid(board, rotated, x, y):
                        shape = rotated
                elif event.key == pygame.K_SPACE:
                    while valid(board, shape, x, y + 1):
                        y += 1

        if fall_timer >= 500:
            fall_timer = 0
            if valid(board, shape, x, y + 1):
                y += 1
            else:
                merge(board, shape, x, y, color)
                board, _ = clear_lines(board)
                shape = random.choice(SHAPES)
                color = random.randrange(1, 8)
                x, y = 3, -len(shape)
                if not valid(board, shape, x, y):
                    running = False

        draw(screen, board, shape, x, y, COLORS[color - 1])

    pygame.quit()


if __name__ == "__main__":
    main()