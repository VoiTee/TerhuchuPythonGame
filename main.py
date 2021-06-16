import pygame
from gamefiles.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, BLACK
from gamefiles.game import Game
from gamefiles.board import Board
from minimax.minimax import minimax
from gamefiles.mcts import MonteCarloTreeSearchNode
from copy import deepcopy
import sys

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Terhuchu')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    sys.setrecursionlimit(10000)

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    #piece = board.get_piece(0,1)
    #board.move(piece, 4, 3)

    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            board = game.get_board()
            temp_board = deepcopy(board)
            root = MonteCarloTreeSearchNode(color = BLACK, board = temp_board)
            selected_node = root.best_action()
            print(board.board)
            board = selected_node.board
            print(board.board)
            print(selected_node)
            game.ai_move()
            # value, new_board = minimax(game.get_board(), 5, BLACK, game)
            # game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

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
