from pygame import *

MOB_HEIGHT = 48


class Mob(sprite.Sprite):
    """
    Конструктор класса Mob

    self.height, self.width - размеры, пересчитанные для вывода на экран
    self.home - начальные координаты
    self.area - max расстояние, которое может пройти в одну сторону
    self.xvel - скорость передвижения по горизонтали

    можно загрузить любой спрайт с названием mob.png, код сам отформатирует
    размер
    """
    def __init__(self, x, y, vel, area):
        sprite.Sprite.__init__(self)
        self.image = image.load("mob.png")
        mob_size = self.image.get_rect().size
        self.height = MOB_HEIGHT
        self.width = self.height * mob_size[0] // mob_size[1]
        self.image = transform.scale(self.image, [self.width, self.height])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.home = x
        self.area = area
        self.xvel = vel

    def update(self, platforms):  # по принципу героя
        """
        Функция перемещения и обновления изображения

        platforms: список платформ
        """
        self.rect.x += self.xvel
        self.bump(platforms)

        if abs(self.home - self.rect.x) > self.area:
            self.xvel *= -1  # если прошли max растояние, то идем обратно

    def bump(self, platforms):
        """
        Функция взаимодействия с платформами (vibe check)

        platforms: список платформ
        """
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                if self.xvel > 0:
                    self.rect.right = p.rect.left

                if self.xvel < 0:
                    self.rect.left = p.rect.right

                self.xvel *= -1  # то поворачиваем в обратную сторону
