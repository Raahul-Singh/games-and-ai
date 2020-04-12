import numpy as np
import random

class Engine:
    def __init__(self, SIZE, WIN_SCORE, player, randomize=True):
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        self.player = player
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.opening_move = (self.SIZE // 2, self.SIZE // 2)
        self.current_move = (-1, -1)
        self.dummy_move = self.opening_move
        self.randomize = randomize
        self.first_move = True

    def reset(self):
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.opening_move = (self.SIZE // 2, self.SIZE // 2)
        self.current_move = (-1, -1)
        self.dummy_move = self.opening_move
        self.first_move = True

    def open_game(self):
        x, y = self.opening_move
        if self.state[x, y] != 0:
            x += 1
            y += 1

        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)
        self.dummy_move = (x, y)
        ## print("In open game\n",self.state,"\n**********")
    def perform_minimax(self):

        if self.first_move:
            self.open_game()
            self.first_move = False
            return

        (x, y), _ = self.minimax(self.state, self.player)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)
        self.dummy_move = self.current_move

    def perform_minimax_alpha_beta_pruning(self):

        if self.first_move:
            self.open_game()
            self.first_move = False
            return

        (x, y), val = self.minimax_alpha_beta_pruning(self.state, self.player, -np.inf, np.inf)
      #  print("value of current move = ", val)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)
        self.dummy_move = self.current_move

    def perform_depth_limited_minimax(self, depth):

        if self.first_move:
            self.open_game()
            self.first_move = False
            return

        (x, y), _ = self.depth_limited_minimax(self.state, self.player, depth)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)
        self.dummy_move = self.current_move

    def perform_depth_limited_alpha_beta_pruning(self, depth):

        if self.first_move:
            self.open_game()
            self.first_move = False
            return

        (x, y), val = self.depth_limited_alpha_beta_pruning(self.state, self.player, depth, -np.inf, np.inf)
        if self.player == 'x':
            self.state[x, y] = 1
        else:
            self.state[x, y] = -1
        self.current_move = (x, y)
        self.dummy_move = self.current_move

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

    def board_traversal(self, state, current_move):

        x, y = current_move
        sum_vertical = 0
        sum_horizontal = 0
        sum_diag = 0
        sum_off_diag = 0

        for i in range(-self.WIN_SCORE + 1, self.WIN_SCORE):
            if 0 <= y + i < self.SIZE:
                sum_vertical = self.update_sum(sum_vertical, state[x, y + i])

            if 0 <= x + i < self.SIZE:
                sum_horizontal =  self.update_sum(sum_horizontal, state[x + i, y])
        
            if 0 <= y + i < self.SIZE and 0 <= x + i < self.SIZE:
                sum_diag = self.update_sum(sum_diag, state[x + i, y + i])

            if 0 <= x + i < self.SIZE and 0 <= y - i < self.SIZE:
                sum_off_diag = self.update_sum(sum_off_diag, state[x + i, y - i])

            if i >= 0:
                for k in [sum_vertical, sum_horizontal, sum_diag, sum_off_diag]:
                    if k == self.WIN_SCORE:
                        return 1 # X Wins
                    elif k == -self.WIN_SCORE:
                        return -1 # O Wins
        return 0

    def update_heuristic_sum(self, a, b):
        return a + b

    def board_traversal_heuristic(self, state, current_move, player):

        x, y = current_move
        sum_vertical_left = state[x, y]
        sum_horizontal_left = state[x, y]
        sum_diag_left = state[x, y]
        sum_off_diag_left = state[x, y]
        sum_vertical_right = state[x, y]
        sum_horizontal_right = state[x, y]
        sum_diag_right = state[x, y]
        sum_off_diag_right = state[x, y]
        heuristic_value = 0

        for i in range(1, 2 * self.WIN_SCORE):

            if y + i < self.SIZE:
                sum_vertical_left = self.update_heuristic_sum(sum_vertical_left, state[x, y + i])

            if x + i < self.SIZE:
                sum_horizontal_left =  self.update_heuristic_sum(sum_horizontal_left, state[x + i, y])

            if y + i < self.SIZE and x + i < self.SIZE:
                sum_diag_left = self.update_heuristic_sum(sum_diag_left, state[x + i, y + i])

            if x + i < self.SIZE and y - i >= 0:
                sum_off_diag_left = self.update_heuristic_sum(sum_off_diag_left, state[x + i, y - i])

            if y - i >= 0:
                sum_vertical_right = self.update_heuristic_sum(sum_vertical_right, state[x, y - i])

            if x - i >= 0:
                sum_horizontal_right =  self.update_heuristic_sum(sum_horizontal_right, state[x - i, y])

            if y - i >= 0 and x - i >= 0:
                sum_diag_right = self.update_heuristic_sum(sum_diag_right, state[x - i, y - i])

            if x - i >= 0 and y + i < self.SIZE:
                sum_off_diag_right = self.update_heuristic_sum(sum_off_diag_right, state[x - i, y + i])

        """
        In the loop below, a higher value of k means a more dense neighbourhood.
        With a move here, you either are either winning or screwing your opponent.
        This helps deal with suboptimal players as well.
        """
        for k in [sum_vertical_left, sum_horizontal_left, sum_diag_left, sum_off_diag_left,
                  sum_vertical_right, sum_horizontal_right, sum_diag_right, sum_off_diag_right]:
            heuristic_value += (k ** 2)

        return heuristic_value

    def evaluation_heuristic(self, state, player):
        heuristic_value = self.board_traversal_heuristic(state, self.dummy_move, player)
        return heuristic_value

    def goal_test(self, state):
        return self.board_traversal(state, self.dummy_move)

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
                self.dummy_move = (x, y)
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
                self.dummy_move = (x, y)
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
                self.dummy_move = (x, y)
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
                self.dummy_move = (x, y)
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
            return (-1, -1), self.evaluation_heuristic(state, player)

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
                self.dummy_move = (x, y)
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
                self.dummy_move = (x, y)
                min_move, min_value = self.depth_limited_minimax(state, 'x', depth-1)
                state[x, y] = 0
                if min_value < best_value:
                    best_value = min_value
                    best_move = action

            return best_move, best_value

    def get_distance(self, square_i):
        return np.sqrt(np.abs(square_i[0] - self.current_move[0]) ** 2 + 
                np.abs(square_i[1] - self.current_move[1]) ** 2)

    def depth_limited_alpha_beta_pruning(self, state, player, depth, alpha, beta):

        if depth == 0:
            return (-1, -1), self.evaluation_heuristic(state, player)

        value = self.goal_test(state)

        if value != 0:
            return (-1, -1), value

        elif player == 'x':
            best_value = -np.inf
            best_move = (-1, -1)
            possible_actions = self.get_actions(state)

            if len(possible_actions) == 0:
                return (-1, -1), 0

            """
            Locality modification : reduces search tree and makes up for stupid opponent
             2 * self.WIN_SCORE - depth is heuristic
            sorting ensures move closeness
            """
            actions = []
            for i in possible_actions:
                if self.get_distance(i) < self.WIN_SCORE:
                    actions.append(i)

            for action in actions:
                x, y = action
                state[x, y] = 1
                self.dummy_move = (x, y)
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
            possible_actions = self.get_actions(state)

            if len(possible_actions) == 0:
                return (-1, -1), 0

            """
            Locality modification : reduces search tree and makes up for stupid opponent
            + 1 is heuristic
            sorting ensures move closeness
            """
            actions = []
            for i in possible_actions:
                if self.get_distance(i) <  self.WIN_SCORE + 1:
                    actions.append(i)

            for action in actions:
                x, y = action
                state[x, y] = -1
                self.dummy_move = (x, y)
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
