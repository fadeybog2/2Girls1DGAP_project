from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
COLOR1 = (200, 180, 0)
COLOR2 = (255, 135, 0)
COLOR3 = (0, 0, 255)


class Wall(sprite.Sprite):
    """
    Конструктор класса Wall

    self.size - размеры
    self.is_free - нельзя на нее ничего спавнить

    self.image - пока прямоугольник, TODO - спрайт
    """
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((self.size[0], self.size[1]))
        self.image.fill(COLOR2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_free = False


class Platform(sprite.Sprite):
    """
    Конструктор класса Platform

    self.size - размеры
    self.is_free - default можно что-то спавнить на

    self.image - пока прямоугольник, TODO - спрайт
    """
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((self.size[0], self.size[1] // 2))
        self.image.fill(COLOR1)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_free = True


class Spike(Platform):
    """
    Конструктор класса Spike, подкласс Platform

    self.is_free - нельзя на него ничего спавнить

    self.image - спрайт с названием spikes.png, любого размера - форматируется
    само
    """
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("spikes.png")
        self.height = 48
        self.width = 48
        self.image = transform.scale(self.image, [self.width, self.height])
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.is_free = False


class Teleport(Platform):
    """
    Конструктор класса Teleport, подкласс Platform

    self.goX, self.goY - координаты назначения телепорта
    self.is_free - нельзя на него ничего спавнить

    self.image - спрайт с названием portal.png любого размера
    """
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.image = image.load("portal.png")
        self.height = 48
        self.width = 48
        self.image = transform.scale(self.image, [self.width, self.height])
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        self.is_free = False
