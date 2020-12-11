from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
COLOR1 = (200, 180, 0)
COLOR2 = (255, 0, 0)
COLOR3 =(0, 0, 255)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((self.size[0], self.size[1]))
        self.image.fill(Color(COLOR1))
        self.rect = self.image.get_rect(topleft=(x, y))

class Spike(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(COLOR2)
        self.rect = Rect(x + PLATFORM_WIDTH / 4, y + PLATFORM_HEIGHT / 4, PLATFORM_WIDTH - PLATFORM_WIDTH / 2, PLATFORM_HEIGHT - PLATFORM_HEIGHT / 2)

class Teleport(Platform):
    def __init__(self, x, y, goX,goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        self.image.fill(COLOR3)
