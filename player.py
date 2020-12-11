from pygame import *
import blocks
import mobs

MOVE_SPEED = 7
HEIGHT = 48
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
        self.image0 = transform.scale(self.image, [self.width, self.height])
        self.image = self.image0
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
            self.image = self.image0

        if right:
            self.vx = MOVE_SPEED  # движение вправо
            self.image = transform.flip(self.image0, 1, 0)

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
                if isinstance(p, blocks.Spike) or isinstance(p, mobs.Mob): # если пересакаемый блок - blocks.BlockDie или Monster
                       self.die()
                elif isinstance(p, blocks.Teleport):
                    self.teleporting(p.goX, p.goY)

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

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
        
    def die(self):
        time.wait(1000)
        self.xvel = 0
        self.yvel = 0
        self.teleporting(self.startX, self.startY) # перемещаемся в начальные ко
