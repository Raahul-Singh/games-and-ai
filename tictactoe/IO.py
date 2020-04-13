import pygame


class BasicInput():

    def __init__(self, *, x, y, w, h, COLOR_INACTIVE='lightskyblue3', COLOR_ACTIVE='dodgerblue2',
                 FONT_STYLE="Times New Roman", FONT_COLOR='black', FONT_SIZE=25, defining_text='', text_offset=10,
                ):
        self.rect = pygame.Rect(x, y, w+2, h+2)
        self.FONT = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        self.defining_text = defining_text
        self.defining_text_surface = self.FONT.render(self.defining_text, True, pygame.Color(FONT_COLOR))
        self.defining_text_pos = (text_offset, self.rect.y)
        self.active = False

        if isinstance(COLOR_INACTIVE, tuple):
            r, g, b, a = COLOR_INACTIVE
            self.COLOR_INACTIVE = pygame.Color(r, g, b, a)
        else:
            self.COLOR_INACTIVE = pygame.Color(COLOR_INACTIVE)

        if isinstance(COLOR_ACTIVE, tuple):
            r, g, b, a = COLOR_ACTIVE
            self.COLOR_ACTIVE = pygame.Color(r, g, b, a)
        else:
            self.COLOR_ACTIVE = pygame.Color(COLOR_ACTIVE)

        self.color = self.COLOR_INACTIVE

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

    def draw(self, screen):
        screen.blit(self.defining_text_surface, self.defining_text_pos)
        pygame.draw.rect(screen, self.color, self.rect, 2)


class NumericalInput(BasicInput):

    def __init__(self, x, y, w, h, defining_text, defining_text_offset, text='', TEXT_COLOR='black'):
        super().__init__(x=x, y=y, w=w, h=h, defining_text=defining_text, text_offset=defining_text_offset)

        self.text = text
        self.TEXT_COLOR = pygame.Color(TEXT_COLOR)
        self.txt_surface = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    try:
                        int(self.text)
                    except ValueError:
                        self.text = "Numerical input required!"
                self.txt_surface = self.FONT.render(self.text, True, self.TEXT_COLOR)
                if self.text == "Numerical input required!":
                    self.text = ''

    def update(self):
        width = max(35, self.txt_surface.get_width() + 20)
        self.rect.w = width

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 3))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class ToggleButton(BasicInput):

    def __init__(self, x, y, w, h, defining_text, defining_text_offset, TEXT_COLOR='black',
                       COLOR_INACTIVE=(255, 0, 0, 20), COLOR_ACTIVE=(0, 255, 0, 20), text_inactive='No', text_active='Yes'):
        super().__init__(x=x, y=y, w=w, h=h, defining_text=defining_text, text_offset=defining_text_offset,
                         COLOR_INACTIVE=COLOR_INACTIVE, COLOR_ACTIVE=COLOR_ACTIVE)
        
        self.TEXT_INACTIVE = text_inactive
        self.TEXT_ACTIVE = text_active
        self.text = self.TEXT_INACTIVE
        self.TEXT_COLOR  = pygame.Color(TEXT_COLOR)
        self.toggle = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        self.text = self.TEXT_ACTIVE if self.active else self.TEXT_INACTIVE
        self.toggle = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def update(self):
        self.rect.w = max(35, self.toggle.get_width() + 20)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.toggle, (self.rect.x + 10, self.rect.y + 3))
        pygame.draw.rect(screen, self.color, self.rect, 2)
