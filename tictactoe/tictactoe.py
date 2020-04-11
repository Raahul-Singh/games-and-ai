import pygame
import numpy as np
from solver import Engine
class Board(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SIZE, WIN_SCORE, players):
        super(Board, self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        self.WIDTH_STEP = self.SCREEN_WIDTH // self.SIZE
        self.HEIGHT_STEP = self.SCREEN_HEIGHT // self.SIZE
        self.CHAR_WIDTH = int(0.60 * self.WIDTH_STEP)
        self.CHAR_HEIGHT = int(0.60 * self.HEIGHT_STEP)
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.welcome_page = pygame.transform.scale(pygame.image.load('welcome.png'),
                                                  (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.x = pygame.transform.scale(pygame.image.load('X.png'),
                                       (self.CHAR_WIDTH, self.CHAR_HEIGHT))
        self.o = pygame.transform.scale(pygame.image.load('O.png'),
                                       (self.CHAR_WIDTH, self.CHAR_HEIGHT))
        self.move_number = 0
        self.players = players

    def welcome_user(self):
        self.screen.blit(self.welcome_page, (0,0))

    def congratulate_winner(self, winner):
        if winner == 'x':
            winner = pygame.transform.scale(pygame.image.load('X.png'),
                                       (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        else:
            winner = pygame.transform.scale(pygame.image.load('O.png'),
                            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(winner, (0,0))

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        self.draw_lines()
        self.update()

    def draw_lines(self):

        for i in range(1, self.SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), 
                            (self.WIDTH_STEP*i, 0), 
                            (self.WIDTH_STEP*i, self.SCREEN_HEIGHT))

            pygame.draw.line(self.screen, (0, 0, 0), 
                            (0, self.HEIGHT_STEP*i), 
                            (self.SCREEN_WIDTH, self.HEIGHT_STEP*i))

    def track_clicks(self, player):
        if not player.is_AI:
            x, y = pygame.mouse.get_pos()
            x = x // self.WIDTH_STEP
            y = y // self.HEIGHT_STEP
        else:
            x, y = player.player_board_interface()

        if player.char is 'x' and self.state[x, y] == 0:
            self.state[x, y] = 1
            self.move_number += 1

        elif player.char is 'o' and self.state[x, y] == 0:
            self.state[x, y] =-1
            self.move_number += 1

        for i in self.players:
            if i.char != player.char and i.is_AI:
                i.board_player_interface(x, y)

        if self.move_number >= 2 * (self.WIN_SCORE-1):
            return self.win_test(x, y)

        return 0

    def update(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.state[i, j] == 1:
                    self.screen.blit(self.x, (self.WIDTH_STEP * i + self.WIDTH_STEP//2 - self.CHAR_WIDTH//2,
                                                self.HEIGHT_STEP * j + self.HEIGHT_STEP//2 - self.CHAR_HEIGHT//2))
                elif self.state[i, j] == -1:
                    self.screen.blit(self.o, (self.WIDTH_STEP * i + self.WIDTH_STEP//2 - self.CHAR_WIDTH//2,
                                    self.HEIGHT_STEP * j + self.HEIGHT_STEP//2 - self.CHAR_HEIGHT//2))

    def reset_board(self):
        self.state = np.zeros((self.SIZE, self.SIZE))
        self.move_number = 0
        for i in self.players:
            if i.is_AI:
                i.player_reset()

    def update_sum(self, a, b):
        if b == 0:
            return 0
        elif a > 0 and b < 0:
            return -1
        elif a < 0 and b > 0:
            return 1
        else:
            return a + b

    def board_traversal(self, state, x, y):
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

    def win_test(self, x, y):
        result = self.board_traversal(self.state, x, y)
        if result > 0 :
            print("X Wins")
            return +1
        elif result < 0:
            print("O Wins")
            return -1
        elif self.move_number == self.SIZE**2:
            print("Game is a Draw")
            return None
        else:
            return 0

class Player(pygame.sprite.Sprite):

    def __init__(self, *, first=True, is_AI=False, SIZE=3, WIN_SCORE=3):
        super(Player, self).__init__()

        if first:
            self.char = 'x'
        else:
            self.char = 'o'

        self.is_AI = is_AI
        self.SIZE = SIZE
        self.WIN_SCORE = WIN_SCORE
        if self.is_AI:
            self.engine = Engine(self.SIZE, self.WIN_SCORE, self.char)

    def board_player_interface(self, x, y):
        self.engine.opponent_move = (x, y)
        if self.char == 'x':
            self.engine.state[x, y] = -1
        else:
            self.engine.state[x, y] = 1

    def player_board_interface(self):
        # self.engine.perform_minimax()
        # self.engine.perform_depth_limited_minimax(depth=3)
        self.engine.perform_depth_limited_alpha_beta_pruning(depth=3)
        # self.engine.perform_minimax_alpha_beta_pruning()
        return self.engine.current_move

    def player_reset(self):
        self.engine.reset()

def main():
    pygame.init()
    running = True
    player_x = Player(first=True,  is_AI=False, SIZE=5, WIN_SCORE=3)
    player_o = Player(first=False, is_AI=False, SIZE=5, WIN_SCORE=3)
    board = Board(800, 800, 5, 3, [player_x, player_o])
    winner  = 0
    board.welcome_user()
    pygame.display.flip()
    
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Start!")
                running = False
        board.welcome_user()
        pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and 
                event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Board Cleared!")
                board.reset_board()

            if winner != 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("New Game!")
                board.welcome_user()
                board.reset_board()
                winner = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.move_number % 2 == 0:
                    winner = board.track_clicks(player_x)
                else:
                    winner = board.track_clicks(player_o)

        if winner is None:
            board.screen.fill((255, 255, 255))
            board.congratulate_winner('o')
            board.congratulate_winner('x')
        elif winner > 0:
            board.screen.fill((255, 255, 255))
            board.congratulate_winner('x')
        elif winner  < 0:
            board.screen.fill((255, 255, 255))
            board.congratulate_winner('o')
        else:
            board.draw_board()
            board.update()

        pygame.display.flip()

    pygame.quit()

main()