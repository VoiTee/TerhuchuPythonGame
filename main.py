import pygame
from gamefiles.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from gamefiles.game import Game
from gamefiles.board import Board
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Terhuchu')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    #piece = board.get_piece(0,1)
    #board.move(piece, 4, 3)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row ,col = get_row_col_from_mouse(pos)
                game.select(row,col)



                pass
        game.update()

    pygame.quit()


main()