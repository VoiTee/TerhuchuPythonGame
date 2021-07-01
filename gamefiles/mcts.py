# https://ai-boson.github.io/mcts/
import numpy as np
from collections import defaultdict

from numpy.core.fromnumeric import cumsum
from gamefiles.constants import BLACK, RED
from copy import deepcopy

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

    def remove_empty_keys(self, d):
        for k in list(d):
            if not d[k]:
                del d[k]

    def _get_all_pieces(self, board):
        pieces_black = board.get_all_pieces(BLACK)
        pieces_red = board.get_all_pieces(RED)
        return pieces_black + pieces_red

    def _get_color_pieces(self, board, color):
        pieces = board.get_all_pieces(color)
        return pieces

    def _is_skip(self, piece, move):
        skipped_row = 0
        skipped_col = 0
        if abs(piece[0] - move[0]) > 1 or abs(piece[1] - move[1]) > 1:
            skipped_row = (piece[0] + move[0]) / 2
            skipped_col = (piece[1] + move[1]) / 2
            return [skipped_row, skipped_col]
        else:
            return False

    def get_legal_actions(self, board):
        print("GET_LEGAL_ACTIONS")
        pieces = self._get_color_pieces(board, self.color)

        legal_actions = {}
        # get_legal_actions()
        for piece in pieces:
            piece_pos = (piece.row, piece.col)
            all_valid_moves = board.get_valid_moves(piece)
            legal_actions[piece_pos] = list(all_valid_moves.keys())

        self.remove_empty_keys(legal_actions)

        return legal_actions

    def untried_actions(self):
        print("UNTRIED_ACTIONS")
        self._untried_actions = self.get_legal_actions(self.board)
        print("self._untried_actions: " + str(self._untried_actions))
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
        print("EXPAND")
        self._untried_actions = self.untried_actions()
        self.remove_empty_keys(self._untried_actions)
        keys = list(self._untried_actions.keys())
        last_key = keys.pop()
        last_move = self._untried_actions[last_key][-1]
        del self._untried_actions[last_key][-1]
        self.remove_empty_keys(self._untried_actions)

        all_pieces = self._get_all_pieces(self.board)

        print("last_key: " + str(last_key))
        print("last_move: " + str(last_move))
        print("self._untried_actions: " + str(self._untried_actions))
        for piece in all_pieces:
            print("PIECE: " + str(piece) + str(piece.row) + str(piece.col))
            if piece.row == last_key[0] and piece.col == last_key[1]:
                our_piece = piece

        self.board.move(our_piece, last_move[0], last_move[1])
        action = { last_key: last_move}
        if self.color == RED:
            color = BLACK
        else:
            color = RED

        temp_board = deepcopy(self.board)
        child_node = MonteCarloTreeSearchNode(
            color, temp_board, parent=self, parent_action=action)

        self.children.append(child_node)

        return child_node 

    def is_terminal_node(self):
        print("IS_TERMINAL_NODE")
        print(self.board.winner())
        return self.board.winner()

    def rollout(self):
        print("ROLLOUT")
        current_rollout_board = self.board

        counter = 1000
        while current_rollout_board.winner() == None and counter:
            counter -= 1
            possible_moves = self.get_legal_actions(current_rollout_board)

            key, move = self.rollout_policy(possible_moves)
            all_pieces = self._get_all_pieces(self.board)
            skip = self._is_skip(key, move)
            for piece in all_pieces:
                if piece.row == key[0] and piece.col == key[1]:
                    our_piece = piece
                    current_rollout_board.move(our_piece, move[0], move[1])
                if skip:
                    if piece.row == skip[0] and piece.col == skip[1]:
                        skipped_piece = piece
                        current_rollout_board.mcts_remove(skipped_piece)

        if counter > 0:
            return current_rollout_board.winner()
        else:
            return BLACK

    def backpropagate(self, result):
        print("BACKPROPAGATE: ")
        for xs in self.board.board:
            print(" ".join(map(str, xs)))
        print("cofansko")
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        print("IS_FULLY_EXPANDED")
        print("is_fully_expanded: " + str(len(self._untried_actions.keys())))
        return len(self._untried_actions.keys()) == 0

    def best_child(self, c_param=0.1):
        print("BEST_CHILD")
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        print("choices_weights: " + str(choices_weights))
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        print("ROLLOUT_POLICY")
        keys = list(possible_moves.keys())
        chosen_key = keys[np.random.randint(len(possible_moves.keys()))]
        # print("chosen_key: " + str(chosen_key) + "possible_moves: " + str(possible_moves))
        chosen_piece = possible_moves[chosen_key]
        # print("chosen_piece: " + str(chosen_piece))
        # count = sum(len(v) for v in chosen_piece.values())

        chosen_move = []
        for i in range(len(chosen_piece)):
            if self._is_skip(chosen_key, chosen_piece[i]):
                chosen_move = chosen_piece[i]

        if not chosen_move:
            chosen_move = chosen_piece[np.random.randint(len(chosen_piece))]

        return chosen_key, chosen_move

    def _tree_policy(self):
        print("_TREE_POLICY")
        current_node = self
        while current_node.is_terminal_node() != RED and current_node.is_terminal_node() != BLACK:
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 5
        for i in range(simulation_no):
            print("SIMULATION " + str(i))
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=1.4)
