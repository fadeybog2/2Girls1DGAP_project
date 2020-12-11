from pygame import *

MOB_WIDTH = 32
MOB_HEIGHT = 32
MOB_COLOR = (200, 200, 200)


class Mob(sprite.Sprite):
    def __init__(self, x, y, vel, area):
        sprite.Sprite.__init__(self)
        self.image = Surface((MOB_WIDTH, MOB_HEIGHT))
        self.image.fill(MOB_COLOR)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.home = x # начальные координаты
        self.area = area # максимальное расстояние, которое может пройти в одну сторону
        self.xvel = vel # cкорость передвижения по горизонтали, 0 - стоит на месте
        
    def update(self, platforms): # по принципу героя
        self.rect.x += self.xvel
        
        self.bump(platforms)
        
        if (abs(self.home - self.rect.x) > self.area):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону

    def bump(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
                if self.xvel > 0:
                    self.rect.right = p.rect.left

                if self.xvel < 0:
                    self.rect.left = p.rect.right

                self.xvel = - self.xvel # то поворачиваем в обратную сторону
