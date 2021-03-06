import pygame
from .constants import BLACK, RED, ROWS, COLS, SQUARE_SIZE, WHITE, GREY
from .piece import Piece
class Board:
    def __init__(self):
        self.board = []
        #self.selected_piece = None
        self.red_left = self.white_left = 8
        self.red_kings = self.white_kings = 0
        self.create_board()


    def draw_cubes(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                #pygame.draw.rect(win,RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(win, GREY, (SQUARE_SIZE * row + SQUARE_SIZE // 2, SQUARE_SIZE * col + SQUARE_SIZE // 2), SQUARE_SIZE//2)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row,col)
        if row == ROWS - 1 or row ==0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings =+ 1

        pass

    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 2:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row > 2:
                    self.board[row].append(Piece(row, col, RED))
                else:
                    self.board[row].append(0)


    def draw(self,win):
        self.draw_cubes(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)


    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

    def get_valid_moves(self, piece):
        moves = {}
        straight_up = piece.col
        straight_down = piece.col
        straight_left = piece.row - 1
        straight_right = piece.row + 1
        diag_left = piece.col - 1
        diag_right = piece.col + 1
        row = piece.row
        col = piece.col

        if piece.color == RED or piece.king:
            #DIAG UP
            moves.update(self._diagonal_left(row - 1, max(row - 3, -1), -1, piece.color, diag_left))
            moves.update(self._diagonal_right(row - 1, max(row - 3, -1), -1, piece.color, diag_right))
            #DIAG DOWN
            moves.update(self._diagonal_left(row + 1, min(row + 3, ROWS), 1, piece.color, diag_left))
            moves.update(self._diagonal_right(row + 1, min(row + 3, ROWS), 1, piece.color, diag_right))
            moves.update(self._vertical(row - 1, min(row - 3, ROWS), -1, piece.color, straight_up)) #UP
            moves.update(self._vertical(row + 1, min(row + 3, ROWS), 1, piece.color, straight_down)) #DOWN
            moves.update(self._horizontal(col - 1, min(col - 3, COLS), -1, piece.color, row)) #LEFT
            moves.update(self._horizontal(col + 1, min(col + 3, COLS), +1, piece.color, row)) #RIGHT

        if piece.color == WHITE or piece.king:
            #DIAG UP
            moves.update(self._diagonal_left(row - 1, max(row - 3, -1), -1, piece.color, diag_left))
            moves.update(self._diagonal_right(row - 1, max(row - 3, -1), -1, piece.color, diag_right))
            #DIAG DOWN
            moves.update(self._diagonal_left(row + 1, min(row + 3, ROWS), 1, piece.color, diag_left))
            moves.update(self._diagonal_right(row + 1, min(row + 3, ROWS), 1, piece.color, diag_right))
            moves.update(self._vertical(row - 1, min(row - 3, ROWS), -1, piece.color, straight_up)) #UP
            moves.update(self._vertical(row + 1, min(row + 3, ROWS), 1, piece.color, straight_down)) #DOWN
            moves.update(self._horizontal(col - 1, min(col - 3, COLS), -1, piece.color, row)) #LEFT
            moves.update(self._horizontal(col + 1, min(col + 3, COLS), +1, piece.color, row)) #RIGHT

        return moves

    def _vertical(self, start, stop, step, color, vert, skipped=[]):
        moves = {}
        last = []


        for r in range(start,stop,step):
            if start < 0 or start > ROWS :
                break

            current = self.board[r][vert]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, vert)] = last + skipped
                else:
                    moves[(r,vert)] = last

                if last:
                    if step == -1:
                        col = max(r - 3, 0)
                    else:
                        col = min(r + 3, ROWS)
                    moves.update(self._vertical(col + step, stop, step, color, vert, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            #vert -= 1

        return moves

    def _horizontal(self, start, stop, step, color, vert, skipped=[]):
        moves = {}
        last = []


        for r in range(start,stop,step):
            if start < 0 or start > COLS :
                break

            current = self.board[vert][r]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(vert, r)] = last + skipped
                else:
                    moves[(vert,r)] = last

                if last:
                    if step == -1:
                        col = max(vert - 3, 0)
                    else:
                        col = min(vert + 3, COLS)
                    moves.update(self._horizontal(col + step, stop, step, color, vert, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            #vert -= 1

        return moves

    def _diagonal_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._diagonal_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._diagonal_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _diagonal_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._diagonal_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._diagonal_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves