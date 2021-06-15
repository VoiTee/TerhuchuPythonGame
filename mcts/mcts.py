# https://ai-boson.github.io/mcts/
import numpy as np
from collections import defaultdict

class MonteCarloTreeSearchNode():
    def __init__(self, color, board, parent=None, parent_action=None):
        self.color = color
        self.board = board
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        pieces = self.board.get_all_pieces(self.color)
        self._untried_actions = self.board.get_valid_moves(pieces)
        return self._untried_actions

    # Difference between wins and loses
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    # Number of times each node is visited
    def n(self):
        return self._number_of_visits

    def expand(self):
        first_key = next(iter(self._untried_actions))
        action = self._untried_actions.pop(first_key)

        piece = self.board.get_piece(row, col)

        next_board = self.board
        next_board.move(action)

        child_node = MonteCarloTreeSearchNode(
            next_board, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 

