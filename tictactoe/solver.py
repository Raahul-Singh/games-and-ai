import numpy as np
import random

class Engine:
    def __init__(self, SIZE, WIN_SCORE, player, randomize=True):
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        self.player = player
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.current_move = (-1, -1)
        self.randomize = randomize

    def perform_minimax(self):
        (x, y), _ = self.minimax(self.state, self.player)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)

    def perform_minimax_alpha_beta_pruning(self):
        (x, y), _ = self.minimax_alpha_beta_pruning(self.state, self.player, -np.inf, np.inf)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)

    def perform_depth_limited_minimax(self, depth):
        (x, y), _ = self.depth_limited_minimax(self.state, self.player, depth)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)

    def perform_depth_limited_alpha_beta_pruning(self, depth):
        (x, y), _ = self.depth_limited_alpha_beta_pruning(self.state, self.player, depth, -np.inf, np.inf)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)

    def get_actions(self, state):
        actions = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.state[i, j] == 0:
                    actions.append((i,j))
        if self.randomize:
            actions = random.sample(actions, len(actions))
        return actions

    def update_sum(self, a, b):
        if b == 0:
            return 0
        elif a > 0 and b < 0:
            return -1
        elif a < 0 and b > 0:
            return 1
        else:
            return a + b

    def board_traversal(self, state):
        sum = 0
        sum_transposed = 0
        sum_diag1 = 0
        sum_diag2 = 0
        sum_off_diag1 = 0
        sum_off_diag2 = 0

        for i in range(self.SIZE):
            for j in range(self.SIZE):

                sum = self.update_sum(sum, state[i, j])
                sum_transposed =  self.update_sum(sum_transposed, state[j, i])

                if not (j+i >= self.SIZE):
                    sum_diag1 = self.update_sum(sum_diag1, state[j, j + i])
                    sum_diag2 = self.update_sum(sum_diag2, state[j + i, j])
                    sum_off_diag1 = self.update_sum(sum_off_diag1, state[i + j, self.SIZE - j - 1])
                    sum_off_diag2 = self.update_sum(sum_off_diag2, state[j, self.SIZE - j - i - 1])

                for k in [sum, sum_transposed, sum_diag1, sum_diag2, sum_off_diag1, sum_off_diag2]:
                    if k == self.WIN_SCORE:
                        return 1 # X Wins
                    elif k == -self.WIN_SCORE:
                        return -1 # O Wins

            sum = 0
            sum_transposed = 0
            sum_diag1 = 0
            sum_diag2 = 0
            sum_off_diag1 = 0
            sum_off_diag2 = 0

        return 0

    def board_traversal_heuristic(self, state, player):
        """
        adding states as squares of contigous values discounted by linear scale of opposite values

        """
        sum = 0
        sum_transposed = 0
        sum_diag1 = 0
        sum_diag2 = 0
        sum_off_diag1 = 0
        sum_off_diag2 = 0
        heuristic_value = 0

        for i in range(self.SIZE):
            for j in range(self.SIZE):

                sum = self.update_sum(sum, state[i, j])
                sum_transposed =  self.update_sum(sum_transposed, state[j, i])

                if not (j+i >= self.SIZE):
                    sum_diag1 = self.update_sum(sum_diag1, state[j, j + i])
                    sum_diag2 = self.update_sum(sum_diag2, state[j + i, j])
                    sum_off_diag1 = self.update_sum(sum_off_diag1, state[i + j, self.SIZE - j - 1])
                    sum_off_diag2 = self.update_sum(sum_off_diag2, state[j, self.SIZE - j - i - 1])

                for k in [sum, sum_transposed, sum_diag1, sum_diag2, sum_off_diag1, sum_off_diag2]:
                        if player == 'x':
                                heuristic_value -= (self.WIN_SCORE - k) ** 2
                        elif player == 'o':
                                heuristic_value += (self.WIN_SCORE + k) ** 2

            sum = 0
            sum_transposed = 0
            sum_diag1 = 0
            sum_diag2 = 0
            sum_off_diag1 = 0
            sum_off_diag2 = 0

        return heuristic_value


    def evaluation_heuristic(self, state, player):
        return self.board_traversal_heuristic(state, player)


    def goal_test(self, state):
        return self.board_traversal(state)
    
    def minimax(self, state, player):
        value = self.goal_test(state)

        if value != 0:
            return (-1, -1), value

        elif player == 'x':
            best_value = -np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = 1
                max_move, max_value = self.minimax(state, 'o')
                state[x, y] = 0

                if max_value > best_value:
                    best_value = max_value
                    best_move = action

            return best_move, best_value

        else:
            best_value = np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = -1
                min_move, min_value = self.minimax(state, 'x')
                state[x, y] = 0
                if min_value < best_value:
                    best_value = min_value
                    best_move = action

            return best_move, best_value

    def minimax_alpha_beta_pruning(self, state, player, alpha, beta):
        value = self.goal_test(state)

        if value != 0:
            return (-1, -1), value

        elif player == 'x':
            best_value = -np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = 1
                max_move, max_value = self.minimax_alpha_beta_pruning(state, 'o', alpha, beta)
                state[x, y] = 0

                if max_value > best_value:
                    best_value = max_value
                    best_move = action

                if max_value < alpha:
                    alpha = max_value
                
                if alpha >= beta:
                    break

            return best_move, best_value

        else:
            best_value = np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = -1
                min_move, min_value = self.minimax_alpha_beta_pruning(state, 'x', alpha, beta)
                state[x, y] = 0
                if min_value < best_value:
                    best_value = min_value
                    best_move = action

                if min_value < beta:
                    beta = min_value

                if alpha >= beta:
                    break

            return best_move, best_value


    def depth_limited_minimax(self, state, player, depth):

        if depth == 0:
            return (-1, -1), self.board_traversal_heuristic(state, player)

        value = self.goal_test(state)

        if value != 0:
            return (-1, -1), value

        elif player == 'x':
            best_value = -np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = 1
                max_move, max_value = self.depth_limited_minimax(state, 'o', depth-1)
                state[x, y] = 0

                if max_value > best_value:
                    best_value = max_value
                    best_move = action

            return best_move, best_value

        else:
            best_value = np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = -1
                min_move, min_value = self.depth_limited_minimax(state, 'x', depth-1)
                state[x, y] = 0
                if min_value < best_value:
                    best_value = min_value
                    best_move = action

            return best_move, best_value

    def depth_limited_alpha_beta_pruning(self, state, player, depth, alpha, beta):

        if depth == 0:
            return (-1, -1), self.board_traversal_heuristic(state, player)

        value = self.goal_test(state)

        if value != 0:
            return (-1, -1), value

        elif player == 'x':
            best_value = -np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = 1
                max_move, max_value = self.depth_limited_alpha_beta_pruning(state, 'o', depth-1, alpha, beta)
                state[x, y] = 0

                if max_value > best_value:
                    best_value = max_value
                    best_move = action

                if max_value > alpha:
                    alpha = max_value
                
                if alpha >= beta:
                    break

            return best_move, best_value

        else:
            best_value = np.inf
            best_move = (-1, -1)
            actions = self.get_actions(state)

            if len(actions) == 0:
                return (-1, -1), 0

            for action in actions:
                x, y = action
                state[x, y] = -1
                min_move, min_value = self.depth_limited_alpha_beta_pruning(state, 'x', depth-1, alpha, beta)
                state[x, y] = 0

                if min_value < best_value:
                    best_value = min_value
                    best_move = action

                if min_value < beta:
                    beta = min_value
                
                if alpha >= beta:
                    break

            return best_move, best_value
