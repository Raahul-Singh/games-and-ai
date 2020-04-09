import numpy as np
import random

class Engine:
    def __init__(self, SIZE, WIN_SCORE, player):
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        self.player = player
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.current_move = (-1, -1)

    def perform_action(self):
        (x, y), _ = self.minimax(self.state, self.player)
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


"""
    def minimax(self, state, player):
        value = self.goal_test(state)

        if player == 'x':
            best = [-1, -1, -np.inf]
        else:
            best = [-1, -1, +np.inf]

        if value != 0:
            return [-1, -1, value]

        actions = self.get_actions(state)
        if len(actions) == 0:
            return [-1, -1, 0]

        for cell in actions:
            x, y = cell
            state[x][y] = 1 if player == 'x' else -1
            score = self.minimax(state, 'o' if player == 'x' else 'x')
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == 'x':
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

"""