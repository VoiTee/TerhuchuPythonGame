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

    def remove_empty_keys(self, d):
        for k in list(d):
            if not d[k]:
                del d[k]
    def get_legal_actions(self, board):
        pieces = board.get_all_pieces(self.color)
        legal_actions = {}
        # get_legal_actions()
        for piece in pieces:
            piece_pos = (piece.row, piece.col)
            all_valid_moves = board.get_valid_moves(piece)
            legal_actions[piece_pos] = list(all_valid_moves.keys())

        self.remove_empty_keys(legal_actions)
        print("legal_actions: " + str(legal_actions))

        return legal_actions

    def untried_actions(self):
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
        keys = list(self._untried_actions.keys())
        last_key = keys.pop()
        # last_key = (0,2)
        last_move = self._untried_actions[last_key][-1]
        del self._untried_actions[last_key][-1]
        self.remove_empty_keys(self._untried_actions)

        print("_untried_actions: " + str(self._untried_actions))

        all_pieces = self.board.get_all_pieces(self.color)
        for piece in all_pieces:
            if piece.row == last_key[0] and piece.col == last_key[1]:
                our_piece = piece
        # print("all_pieces: " + str(all_pieces))

        print("our_piece: " + str(our_piece.row) + ", " + str(our_piece.col))
        print("last_move: " + str(last_move))

        self.board.move(our_piece, last_move[0], last_move[1])
        action = { last_key: last_move}
        child_node = MonteCarloTreeSearchNode(
            self.color, self.board, parent=self, parent_action=action)

        self.children.append(child_node)

        return child_node 

    def is_terminal_node(self):
        return self.board.winner()

    def rollout(self):
        current_rollout_board = self.board

        while not current_rollout_board.winner():
            possible_moves = self.get_legal_actions(current_rollout_board)

            key, move = self.rollout_policy(possible_moves)
            print("key: " + str(key) + "move: " + str(move))
            all_pieces = self.board.get_all_pieces(self.color)
            for piece in all_pieces:
                if piece.row == key[0] and piece.col == key[1]:
                    our_piece = piece

            current_rollout_board = current_rollout_board.move(our_piece, move[0], move[1])

        return current_rollout_board.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions.keys()) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        keys = list(self._untried_actions.keys())
        chosen_key = keys[np.random.randint(len(possible_moves.keys()))]
        chosen_piece = possible_moves[chosen_key]
        print("chosen_piece: " + str(chosen_piece))
        # count = sum(len(v) for v in chosen_piece.values())
        chosen_move = chosen_piece[np.random.randint(len(chosen_piece))]
        return chosen_key, chosen_move

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)
