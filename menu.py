import pygame as pg

BLACK = (0, 0, 0)
MAROON = (128, 0, 0)
WHITE = (255, 255, 255)
TEXT_COLOR = (255, 0, 255)


class Button:
    '''
    Класс кнопок для меню
    '''

    def __init__(self, screen, x, y, color, name):

        '''
        Конструктор класса кнопок

        self.screen - экран рисования
        self.x - абсцисса верхнего левого угла
        self.y - ордината верхнего левого угла
        self.name - надпись на кнопке
        f = pg.font.Font(None, 50) - шрифт текста на кнопке
        self.w_x, self.w_y - ширина и высота кнопки, определяющаяся длинной и
        высотой текста (т.е. размером шрифта и длиной слова)
        self.color - цвет кнопки
        self.click - показывает, нажата кнопка или нет
        '''

        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        f = pg.font.Font(None, 50)
        (self.w_x, self.w_y) = f.size(self.name)
        self.color = color
        self.click = False

    def draw(self, color_of_text):
        '''
        Функция рисования кнопки
        Рисует черный прямоугольник с текстом заданного цвета

        color_of_text - цвет текста
        '''
        pg.draw.rect(self.screen, self.color, (self.x, self.y,
                                               self.w_x + 10, self.w_y + 10))
        rect_center = (self.x + (self.w_x + 10) // 2,
                       self.y + (self.w_y + 10) // 2)
        f = pg.font.Font(None, 36)
        text = f.render(self.name, True, color_of_text)
        text_rect = text.get_rect(center=rect_center)
        self.screen.blit(text, text_rect)

    def hitting(self, x_m, y_m):
        '''
        Функция определяет, попали ли мы по кнопке или нет
        '''
        if self.x <= x_m <= self.x + self.w_x + 10 and \
                self.y <= y_m <= self.y + self.w_y + 10:
            self.click = True


def start_screen(screen, back, SCREEN_WIDTH, SCREEN_HEIGHT, buttons):
    '''
    Функция отрисовки начального экрана. Включает в себя отрисовку:
    back - фоновая картинка, загружается из файла
    buttons - 2 кнопки, отвечающие за правила и за начало игры
    а также отрисовка названия игры
    переменные SCREEN_WIDTH, SCREEN_HEIGHT используются для масштабирования
    фона, screen - экран для рисования
    '''
    # Масштабирование и отрисовка фона
    back_height = SCREEN_HEIGHT
    size = back.get_rect().size
    back_width = size[0] * back_height // size[1]
    back = pg.transform.scale(back, [back_width, back_height])
    back_rect = back.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(back, back_rect)
    # Пишет название игры
    font = pg.font.Font(None, 64)
    (width_x, width_y) = font.size('Bowling for your life')
    start_x, start_y = 220, 180
    pg.draw.rect(screen, BLACK, (start_x, start_y,
                                 width_x + 10, width_y + 10))
    rect_center = (start_x + (width_x + 10) // 2, start_y + (width_y + 10) // 2)
    text = font.render('Bowling for your life', True, (0, 255, 255))
    text_rect = text.get_rect(center=rect_center)
    screen.blit(text, text_rect)
    # Цикл для отрисовки кнопок
    for button in buttons:
        button.draw(TEXT_COLOR)


def manual_draw(screen, back, SCREEN_WIDTH, SCREEN_HEIGHT, button):
    '''
    Функция отрисовки руководства. Так же, как и в предыдущей есть фон, текст и
    кнопка (в этот раз одна)
    Кнопка выбрасывает обратно на старотовый экран
    SCREEN_WIDTH, SCREEN_HEIGHT опять же используются для масштабирования
    screen - экран отрисовки
    '''
    # Масштабирование и отрисовка все той же фоновой картинки
    back_height = SCREEN_HEIGHT
    size = back.get_rect().size
    back_width = size[0] * back_height // size[1]
    back = pg.transform.scale(back, [back_width, back_height])
    back_rect = back.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(back, back_rect)
    # читаем из файла руководство и зачем-то выводим на экран
    f = pg.font.Font(None, 25)
    file = open('rules.txt', 'r')
    rules = [line.strip() for line in file]
    i = 0
    # Рисуем черный прямоугольник прямоугольник, чтобы буквы видно было
    pg.draw.rect(screen, BLACK, (89, 89, 600, 471))
    # Цикл отрисовки всех надписей построчно
    for rule in rules:
        text = f.render(rule, True,
                        (255, 255, 255))
        screen.blit(text, (100, 100 + 35 * i))
        i += 1
    # Рисуем кнопочку quit
    button.draw(WHITE)
