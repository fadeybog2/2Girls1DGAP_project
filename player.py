from pygame import *

MOVE_SPEED = 7
HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 0.5


class Player(sprite.Sprite):
    def __init__(self, x, y):
        """
        Конструктор класса Player

        self.vx, self.vy - скорость в проекции на горизонталь и вертикаль
        self.startX, self.startY = x, y - начальные координаты
        self.onGround = False - переменная, отслеживающая нахождение на земле

        можно загрузить любой спрайт с названием hero.png, код сам отформатирует
        размер
        """
        sprite.Sprite.__init__(self)
        self.image = image.load("hero.png")
        hero_size = self.image.get_rect().size
        self.height = HEIGHT
        self.width = self.height * hero_size[0] // hero_size[1]
        self.image = transform.scale(self.image, [self.width, self.height])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = self.vy = 0
        self.startX, self.startY = x, y
        self.onGround = False

    def update(self, left, right, up, platforms):
        """
        Функция обработки нажатия клавиш

        left: управление движением влево
        right: управление движением вправо
        up: прыжок
        platforms: список платформ
        """

        if up:
            if self.onGround:
                # двойной прыжок не прописан, прыгает только с земли
                self.vy = -JUMP_POWER

        if left:
            self.vx = -MOVE_SPEED  # движение влево

        if right:
            self.vx = MOVE_SPEED  # движение вправо

        if not (left or right):  # стоит чиллит
            self.vx = 0

        if not self.onGround:
            # изменение скорости в прыжке
            self.vy += GRAVITY

        self.onGround = False
        self.rect.y += self.vy
        self.bump(0, self.vy, platforms)

        self.rect.x += self.vx  # движение игрока на Vx
        self.bump(self.vx, 0, platforms)

    def bump(self, vx, vy, platforms):
        """
        Функция взаимодействия с платформами (vibe check)

        vx: скорость по горизонтали
        vy: скорость по вертикали
        platforms: список платформ
        """
        for p in platforms:
            if sprite.collide_rect(self, p):
                # проверка столкновения с платформой

                if vx > 0:
                    self.rect.right = p.rect.left

                if vx < 0:
                    self.rect.left = p.rect.right

                if vy > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True  # теперь он на земле
                    self.vy = 0

                if vy < 0:
                    self.rect.top = p.rect.bottom  # не может пробить платформу
                    self.vy = 0
