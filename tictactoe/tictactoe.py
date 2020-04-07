import pygame
import numpy as np

class Board(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SIZE, WIN_SCORE):
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
        x, y = pygame.mouse.get_pos()
        x = x // self.WIDTH_STEP
        y = y // self.HEIGHT_STEP

        if player.char is 'x' and self.state[x, y] == 0:
            self.state[x, y] = 1
            self.move_number += 1

        elif player.char is 'o' and self.state[x, y] == 0:
            self.state[x, y] =-1
            self.move_number += 1

        if self.move_number >= 2 * (self.WIN_SCORE-1):
            return self.win_test()
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

    def update_sum(self, a, b):
        if b == 0:
            return 0
        elif a > 0 and b < 0:
            return -1
        elif a < 0 and b > 0:
            return 1
        else:
            return a + b

    def board_traversal(self):
        sum = 0
        sum_transposed = 0
        sum_diag1 = 0
        sum_diag2 = 0
        sum_off_diag1 = 0
        sum_off_diag2 = 0

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                sum += self.state[i, j]
                sum_transposed += self.state[j, i]
                if sum == self.WIN_SCORE or sum_transposed == self.WIN_SCORE:
                    return 1 # X Wins
                elif sum == -self.WIN_SCORE or sum_transposed == -self.WIN_SCORE:
                    return -1 # O Wins
            sum = 0
            sum_transposed = 0

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if j+i >= self.SIZE:
                    break

                sum_diag1 = self.update_sum(sum_diag1, self.state[j, j + i])
                sum_diag2 = self.update_sum(sum_diag2, self.state[j + i, j])
                sum_off_diag1 = self.update_sum(sum_off_diag1, self.state[i + j, self.SIZE - j - 1])
                sum_off_diag2 = self.update_sum(sum_off_diag2, self.state[j, self.SIZE - j - i - 1])

                for k in [sum_diag1, sum_diag2, sum_off_diag1, sum_off_diag2]:
                    if k == self.WIN_SCORE:
                        return 1 # X Wins
                    elif k == -self.WIN_SCORE:
                        return -1 # O Wins
            sum_diag1 = 0
            sum_diag2 = 0
            sum_off_diag1 = 0
            sum_off_diag2 = 0
        return 0

    def win_test(self):
        result = self.board_traversal()
        if result > 0 :
            print("X Wins")
            return +1
        elif result < 0:
            print("O Wins")
            return -1
        else:
            return 0

class Player(pygame.sprite.Sprite):

    def __init__(self, first=True, width=80, height=100):
        super(Player, self).__init__()
            
        if first:
            self.char = 'x'
        else:
            self.char = 'o'
 

def main():
    pygame.init()
    running = True
    board = Board(720, 720, 3, 3)
    player_x = Player(first=True)
    player_o = Player(first=False)
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
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Board Cleared!")
                board.reset_board()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.move_number % 2 == 0:
                    winner = board.track_clicks(player_x)
                    if winner > 0:
                        board.screen.fill((255, 255, 255))
                        board.congratulate_winner('x')
                else:
                    winner = board.track_clicks(player_o)
                    if winner  < 0:
                        board.screen.fill((255, 255, 255))
                        board.congratulate_winner('o')
        if winner == 0:
            board.draw_board()
            board.update()

        pygame.display.flip()

    pygame.quit()

main()