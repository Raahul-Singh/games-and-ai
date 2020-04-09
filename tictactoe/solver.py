import numpy as np
import random

class Solver:
    def __init__(self, char, SIZE, WIN_SCORE):
        self.char = char
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.current_move = None
        self.move_number = 0

    def board_player_interface(self, x, y):
        if self.char == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1

    def player_board_interface(self):
        self.make_best_move()
        return self.current_move

    def make_best_move(self):
        _, self.current_move = self.minimax(self.state,
                                            0 if self.char == 'x' else 1)
        self.state = self.perform_action(self.state, self.current_move)
        self.move_number += 1

    def get_child(self, state, action):
        return self.generate_state(state, action)

    def generate_state(self, parent_state, action):
        new_state = np.copy(parent_state)
        return self.perform_action(new_state, action)

    def perform_action(self, state, action):
        x, y = action
        if self.char == 'x':
            state[x, y] = 1
        elif self.char == 'o':
            state[x, y] = -1
        return state

    def get_actions(self, state):
        actions = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.check_if_valid_move(i, j, state):
                    actions.append((i, j))
        return actions

    def check_if_valid_move(self, x, y, state):
        return state[x, y] == 0

    def goal_test(self, state):
        result = self.board_traversal(state)
        if result > 0:
            return +1
        elif result < 0:
            return -1
        elif self.SIZE % 2 != 0:
            if self.char == 'x' and self.move_number == (self.SIZE ** 2 - 1) // 2 + 1:
                return 0
            elif self.char == 'o' and self.move_number == (self.SIZE ** 2 - 1) // 2:
                return 0
        elif self.SIZE % 2 == 0 and self.move_number == (self.SIZE ** 2) // 2:
            return 0
        else:
            return None

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

                sum = self.update_sum(sum, self.state[i, j])
                sum_transposed =  self.update_sum(sum_transposed, self.state[j, i])

                if not (j+i >= self.SIZE):
                    sum_diag1 = self.update_sum(sum_diag1, self.state[j, j + i])
                    sum_diag2 = self.update_sum(sum_diag2, self.state[j + i, j])
                    sum_off_diag1 = self.update_sum(sum_off_diag1, self.state[i + j, self.SIZE - j - 1])
                    sum_off_diag2 = self.update_sum(sum_off_diag2, self.state[j, self.SIZE - j - i - 1])

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

    def minimax(self, state, move_number):
        value = self.goal_test(state)

        if value != None:
            return value, None

        elif move_number % 2 == 0:
            actions = self.get_actions(state)
            best_value = -np.inf
            best_move = None

            for action in actions:
                child = self.get_child(state, action)
                minimax_value, minimax_move = self.minimax(child, move_number+1)
                if minimax_value > best_value:
                    best_move = action
                    best_value = minimax_value

            return minimax_value, best_move

        else:
            actions = self.get_actions(state)
            best_value = np.inf
            best_move = None

            for action in actions:
                child = self.get_child(state, action)
                minimax_value, minimax_move = self.minimax(child, move_number+1)
                if minimax_value < best_value:
                    best_move = action
                    best_value = minimax_value

            return best_value, best_move

    def randomized_minimax(self, state, move_number):
        value = self.goal_test(state)

        if value != 0:
            return value, None

        elif move_number % 2 == 0:
            actions = self.get_actions(state)
            action = random.sample(actions, len(actions))
            best_value = -np.inf
            best_move = None
            for action in actions:
                child = self.get_child(state, action)
                minimax_value, minimax_move = self.minimax(child, move_number+1)
                if minimax_value > best_value:
                    best_move = action
                    best_value = minimax_value

            return minimax_value, best_move
        else:
            actions = self.get_actions(state)
            action = random.sample(actions, len(actions))
            best_value = np.inf
            best_move = None
            for action in actions:
                child = self.get_child(state, action)
                minimax_value, minimax_move = self.minimax(child, move_number+1)
                if minimax_value < best_value:
                    best_move = action
                    best_value = minimax_value

            return best_value, best_move
