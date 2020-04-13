import pygame
import numpy as np
from solver import Engine
from IO import *

class IO():
    
    def __init__(self, SCREEN_WIDTH=800, SCREEN_HEIGHT=800):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
    
    def welcome_user(self):
        welcome_font = pygame.font.SysFont('Times New Roman', 50)
        welcome_text = welcome_font.render("Press any key to Continue!", True, pygame.Color('black'))

        welcome_page = pygame.transform.scale(pygame.image.load('welcome.png'),
                                            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        welcome_text_background = pygame.Surface((welcome_text.get_width() + 20, welcome_text.get_height() + 20))
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        running = True

        while(running):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("Start!")
                    running = False
            screen.blit(welcome_page, (0,0))

            pygame.draw.rect(screen, (255, 255, 255), 
                             welcome_text_background.get_rect(x=(self.SCREEN_WIDTH - welcome_text.get_width()) // 2 - 10, 
                                                              y=self.SCREEN_HEIGHT - 210))

            screen.blit(welcome_text, ((self.SCREEN_WIDTH - welcome_text.get_width()) // 2,
                                        self.SCREEN_HEIGHT - 200))
            pygame.display.flip()

    def get_configuration(self):
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        configuration_font = pygame.font.SysFont('Times New Roman', 32)
        heading = configuration_font.render("System Setup!", True, pygame.Color('black'))
        warn = False
        warning = configuration_font.render("Please fix Input!", True, pygame.Color('black'))
        clock = pygame.time.Clock()
        board_size = NumericalInput(self.SCREEN_WIDTH * 0.60, self.SCREEN_HEIGHT * 0.30, 50, 32, "Board Size ?", 30)
        win_score = NumericalInput(self.SCREEN_WIDTH * 0.60, self.SCREEN_HEIGHT * 0.40, 50, 32, "Win Score ?", 30)
        player_x = ToggleButton(self.SCREEN_WIDTH * 0.60, self.SCREEN_HEIGHT * 0.50, 50, 32, "Is player X an AI?", 30)
        player_y = ToggleButton(self.SCREEN_WIDTH * 0.60, self.SCREEN_HEIGHT * 0.60, 50, 32, "Is player O an AI?", 30)
        submit = ToggleButton(self.SCREEN_WIDTH * 0.55, self.SCREEN_HEIGHT * 0.80, 50, 32, "Submit ?", self.SCREEN_WIDTH * 0.50 - 85)
        input_boxes = [board_size, win_score, player_x, player_y, submit]
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            screen.fill((255, 255, 255))
            for box in input_boxes:
                box.draw(screen)

            if submit.active:
                try:
                    board_size.text = int(board_size.text)
                    win_score.text = int(win_score.text)
                    running = False
                except ValueError:
                    submit.active = False
                    warn = True

            if warn:
                screen.blit(warning, ((self.SCREEN_WIDTH - warning.get_width()) // 2, self.SCREEN_HEIGHT * 0.20))
        
            screen.blit(heading, ((self.SCREEN_WIDTH - heading.get_width()) // 2, self.SCREEN_HEIGHT * 0.10))
            pygame.display.flip()
            clock.tick(30)

        return (board_size.text, win_score.text, player_x.active, player_y.active)
    
    def postgame(self, winner, x_score=0, o_score=0, draw=0):
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        configuration_font = pygame.font.SysFont('Times New Roman', 32)
        
        win_text = "This round was a draw!"
        if winner == 1:
            win_text = "X won this round!"
        elif winner == -1:
            win_text = "O won this round!"

        current_winner = configuration_font.render(win_text, True, pygame.Color('black'))

        heading = configuration_font.render("   Overall Score", True, pygame.Color('black'))
        x_score = configuration_font.render(f"X Won      {x_score} times", True, pygame.Color('black'))
        o_score = configuration_font.render(f"O Won      {o_score} times", True, pygame.Color('black'))
        draw = configuration_font.render(f"Game Drawn    {draw} times", True, pygame.Color('black'))

        clock = pygame.time.Clock()
        replay = ToggleButton(self.SCREEN_WIDTH * 0.20, self.SCREEN_HEIGHT * 0.80, 50, 32,"", 0, text_inactive="Click to replay!")
        end = ToggleButton(self.SCREEN_WIDTH * 0.60, self.SCREEN_HEIGHT * 0.80, 50, 32,"", 0, text_inactive="Click to end!")
        input_boxes = [replay, end]
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for box in input_boxes:
                    box.handle_event(event)
                    if replay.active:
                        return 1
                        running = False
                    elif end.active:
                        running = False
                        return 0

            for box in input_boxes:
                box.update()

            screen.fill((255, 255, 255))
            for box in input_boxes:
                box.draw(screen)

            screen.blit(current_winner, ((self.SCREEN_WIDTH - current_winner.get_width()) // 2, self.SCREEN_HEIGHT * 0.20))
            screen.blit(heading, ((self.SCREEN_WIDTH - heading.get_width()) // 2, self.SCREEN_HEIGHT * 0.30))
            screen.blit(x_score, ((self.SCREEN_WIDTH - x_score.get_width()) // 2, self.SCREEN_HEIGHT * 0.40))
            screen.blit(o_score, ((self.SCREEN_WIDTH - o_score.get_width()) // 2, self.SCREEN_HEIGHT * 0.50))
            screen.blit(draw, ((self.SCREEN_WIDTH - draw.get_width()) // 2, self.SCREEN_HEIGHT * 0.60))
            pygame.display.flip()
            clock.tick(30)

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
        self.x = pygame.transform.scale(pygame.image.load('X.png'),
                                       (self.CHAR_WIDTH, self.CHAR_HEIGHT))
        self.o = pygame.transform.scale(pygame.image.load('O.png'),
                                       (self.CHAR_WIDTH, self.CHAR_HEIGHT))
        self.move_number = 0
        self.players = players

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

class Player():

    def __init__(self, *, first=True, is_AI=False, SIZE=3, WIN_SCORE=3):

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

class Game():
    def __init__(self):
        self.io = IO()
        self.io.welcome_user()
        board_size, win_score, x_ai, o_ai = self.io.get_configuration()
        self.player_x = Player(first=True,  is_AI=x_ai, SIZE=board_size, WIN_SCORE=win_score)
        self.player_o = Player(first=False, is_AI=o_ai, SIZE=board_size, WIN_SCORE=win_score)
        self.board = Board(800, 800, board_size, win_score, [self.player_x, self.player_o])
        self.x_score = 0
        self.o_score = 0
        self.draw_score = 0
        self.winner  = 0
        self.postgame = None

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                    event.type == pygame.KEYDOWN and 
                    event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.board.reset_board()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.board.move_number % 2 == 0:
                        self.winner = self.board.track_clicks(self.player_x)
                    else:
                        self.winner = self.board.track_clicks(self.player_o)

            if self.winner is None:
                self.draw_score += 1
                self.postgame = self.io.postgame(self.winner, self.x_score, self.o_score, self.draw_score)
                running = False
            elif self.winner > 0:
                self.x_score += 1
                self.postgame = self.io.postgame(self.winner, self.x_score, self.o_score, self.draw_score)
                running = False
            elif self.winner  < 0:
                self.o_score += 1
                self.postgame = self.io.postgame(self.winner, self.x_score, self.o_score, self.draw_score)
                running = False
            else:
                self.board.draw_board()
                self.board.update()

            pygame.display.flip()

        self.post_game()

    def post_game(self):
        # print("in post_game val = ",self.postgame)
        if self.postgame == 1:
            self.new_game()
    
    def new_game(self):
        self.board.reset_board()
        self.winner = 0
        self.postgame = None
        self.run_game()

def main():
    pygame.init()
    game = Game()
    game.run_game()
    pygame.quit()

main()