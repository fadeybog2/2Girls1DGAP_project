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

    def draw(self):
        pg.draw.rect(self.screen, self.color, (self.x, self.y,
                                               self.w_x + 10, self.w_y + 10))
        rect_center = (self.x + (self.w_x + 10)//2, self.y + (self.w_y + 10)//2)
        print(self.w_x, self.w_y)
        f = pg.font.Font(None, 36)
        text = f.render(self.name, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect_center)
        self.screen.blit(text, text_rect)

    def hitting(self, x_m, y_m):
        if self.x <= x_m <= self.x + self.w_x + 10 and \
                self.y <= y_m <= self.y + self.w_y + 10:
            self.click = True


def start_screen(screen, back, SCREEN_WIDTH, SCREEN_HEIGHT, button):
    back_height = SCREEN_HEIGHT
    size = back.get_rect().size
    back_width = size[0] * back_height // size[1]
    back = pg.transform.scale(back, [back_width, back_height])
    back_rect = back.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(back, back_rect)
    button.draw()
    '''
    if event.type == MOUSEBUTTONDOWN:
        button.hitting(event.pos(0), event(1))
    return button.click '''
