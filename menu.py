import pygame as pg

BLACK = (0, 0, 0)
MAROON = (128, 0, 0)
WHITE = (255, 255, 255)
TEXT_COLOR = (255, 0, 255)


class Button:
    def __init__(self, screen, x, y, color, name):
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        f = pg.font.Font(None, 50)
        (self.w_x, self.w_y) = f.size(self.name)
        self.color = color
        self.click = False

    def draw(self, color_of_text):
        pg.draw.rect(self.screen, self.color, (self.x, self.y,
                                               self.w_x + 10, self.w_y + 10))
        rect_center = (self.x + (self.w_x + 10)//2, self.y + (self.w_y + 10)//2)
        f = pg.font.Font(None, 36)
        text = f.render(self.name, True, color_of_text)
        text_rect = text.get_rect(center=rect_center)
        self.screen.blit(text, text_rect)

    def hitting(self, x_m, y_m):
        if self.x <= x_m <= self.x + self.w_x + 10 and \
                self.y <= y_m <= self.y + self.w_y + 10:
            self.click = True


def start_screen(screen, back, SCREEN_WIDTH, SCREEN_HEIGHT, buttons):
    back_height = SCREEN_HEIGHT
    size = back.get_rect().size
    back_width = size[0] * back_height // size[1]
    back = pg.transform.scale(back, [back_width, back_height])
    back_rect = back.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(back, back_rect)
    font = pg.font.Font(None, 64)
    (width_x, width_y) = font.size('Bowling for your life')
    start_x, start_y = 220, 180
    pg.draw.rect(screen, BLACK, (start_x, start_y,
                                 width_x + 10, width_y + 10))
    rect_center = (start_x + (width_x + 10) // 2, start_y + (width_y + 10) // 2)
    text = font.render('Bowling for your life', True, (0, 255, 255))
    text_rect = text.get_rect(center=rect_center)
    screen.blit(text, text_rect)
    for button in buttons:
        button.draw(TEXT_COLOR)


def manual_draw(screen, back, SCREEN_WIDTH, SCREEN_HEIGHT, button):
    back_height = SCREEN_HEIGHT
    size = back.get_rect().size
    back_width = size[0] * back_height // size[1]
    back = pg.transform.scale(back, [back_width, back_height])
    back_rect = back.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(back, back_rect)
    f = pg.font.Font(None, 25)
    file = open('rules.txt', 'r')
    rules = [line.strip() for line in file]
    i = 0
    pg.draw.rect(screen, BLACK, (89, 89, 600, 471))
    for rule in rules:
        text = f.render(rule, True,
                        (255, 255, 255))
        screen.blit(text, (100, 100+35*i))
        i += 1
    button.draw(WHITE)

