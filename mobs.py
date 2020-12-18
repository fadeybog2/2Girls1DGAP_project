import pygame as pg
from random import randint
import blocks

MOB_HEIGHT = 48


class Mob(pg.sprite.Sprite):
    """
    Конструктор класса Mob

    self.height, self.width - размеры, пересчитанные для вывода на экран
    self.startX, self.startY - начальные координаты
    self.area - max расстояние, которое может пройти в одну сторону
    self.xvel - скорость передвижения по горизонтали
    self.is_alive - жив ли?
    self.is_free - можно ли спавнить что-то ему на голову
    self.got_hit - ударили ли моба недавно (для анимации)
    self.time_hit - время с последнего удара (нужно для анимации)
    self.hp - здоровье, задается рандомным целым числом от 1 до 10

    self.death_sound - звук, издаваемый при смерти, загрузка из файла 
    mobs_death_sound.wav

    можно загрузить любой спрайт с названием mob.png, код сам отформатирует
    размер
    """
    def __init__(self, x, y, area):
        pg.sprite.Sprite.__init__(self)
        self.images = [pg.image.load("mob.png"),
                       pg.image.load("mob_rage.png")]
        for i in range(0, len(self.images) - 1):
            mob_size = self.images[i].get_rect().size
            self.height = MOB_HEIGHT
            self.width = self.height * mob_size[0] // mob_size[1]
            self.images[i] = pg.transform.scale(self.images[i],
                                                [self.width, self.height])
        self.image = self.images[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))

        self.startX, self.startY = x, y
        self.area = area
        self.xvel = randint(0, 2)
        self.death_sound = pg.mixer.Sound('mobs_death_sound.wav')
        self.is_alive = True
        self.is_free = False
        self.got_hit = False
        self.time_hit = 0
        self.hp = randint(1, 10)

    def update(self, platforms, fps, hero):  # по принципу героя
        """
        Функция перемещения и обновления изображения

        platforms: список платформ
        """
        self.rect.x += self.xvel
        self.bump(platforms)

        if abs(self.startX - self.rect.x) > self.area:
            self.xvel *= -1  # если прошли max растояние, то идем обратно
        self.check_if_dead(hero)
        if self.got_hit:
            self.time_hit += 1
            if self.time_hit == 1:
                self.picture_changed(self.images[1])
            elif self.time_hit == fps//3:
                self.picture_changed(self.images[0])
                self.time_hit = 0
                self.got_hit = False

    def bump(self, platforms):
        """
        Функция взаимодействия с платформами (vibe check)

        platforms: список платформ
        """
        for p in platforms:
            if pg.sprite.collide_rect(self, p) and self != p:
                if self.xvel > 0:
                    self.rect.right = p.rect.left

                if self.xvel < 0:
                    self.rect.left = p.rect.right

                self.xvel *= -1  # то поворачиваем в обратную сторону

    def picture_changed(self, image):
        """
        Функция меняет картинку моба, с обычной на "когда ударили" и наоборот

        image: картинка, на которую меняем
        """
        self.image = image

    def check_if_dead(self, hero):
        """
        Функция проверяет жив ли моб
        """
        if self.hp <= 0:
            self.hp = 0
            hero.score += 1  # увеличиваем счет в игре
            self.death_sound.set_volume(0.1)
            self.death_sound.play()
            self.is_alive = False
