import pygame

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)


class Board:
    def __init__(self, width, height, left=10, right=10, cell_size=20):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = left
        self.top = right
        self.cell_size = cell_size
        self.x = 0

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.circle(screen, pygame.Color('red'), (
                    x * self.cell_size + self.left + 0.5 * self.cell_size,
                    y * self.cell_size + self.top + 0.5 * self.cell_size), 22, 2)
                pygame.draw.rect(screen, pygame.Color('white'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = 1 + self.board[cell[1]][cell[0]]
        if self.board[cell[1]][cell[0]] == 3:
            self.board[cell[1]][cell[0]] = 0

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, pos):
        cell = self.get_cell(pos)
        if cell is not None:
            self.on_click(cell)


board = Board(4, 5)
board.set_view(50, 50, 50)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()

pygame.quit()
