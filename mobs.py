from pygame import *
from random import randint
import blocks

MOB_HEIGHT = 48


class Mob(sprite.Sprite):
    """
    Конструктор класса Mob

    self.height, self.width - размеры, пересчитанные для вывода на экран
    self.startX, self.startY - начальные координаты
    self.area - max расстояние, которое может пройти в одну сторону
    self.xvel - скорость передвижения по горизонтали
    self.is_alive - жив ли?
    self.is_free - можно ли спавнить что-то ему на голову
    self.hp - здоровье, задается рандомным целым числом от 1 до 10

    можно загрузить любой спрайт с названием mob.png, код сам отформатирует
    размер
    """
    def __init__(self, x, y, area):
        sprite.Sprite.__init__(self)
        self.image = image.load("mob.png")
        mob_size = self.image.get_rect().size
        self.height = MOB_HEIGHT
        self.width = self.height * mob_size[0] // mob_size[1]
        self.image = transform.scale(self.image, [self.width, self.height])
        self.rect = self.image.get_rect(bottomleft=(x, y))

        self.startX, self.startY = x, y
        self.area = area
        self.xvel = randint(0, 2)
        self.is_alive = True
        self.is_free = False
        self.hp = randint(1, 10)

    def update(self, platforms):  # по принципу героя
        """
        Функция перемещения и обновления изображения

        platforms: список платформ
        """
        self.rect.x += self.xvel
        self.bump(platforms)

        if abs(self.startX - self.rect.x) > self.area:
            self.xvel *= -1  # если прошли max растояние, то идем обратно
        self.check_if_dead()

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

    def check_if_dead(self):
        """
        Функция проверяет жив ли моб
        """
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
