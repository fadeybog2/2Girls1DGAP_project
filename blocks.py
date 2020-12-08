from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
COLOR1 = (200, 180, 0)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.size = (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.image = Surface((self.size[0], self.size[1]))
        self.image.fill(Color(COLOR1))
        self.rect = self.image.get_rect(topleft=(x, y))
