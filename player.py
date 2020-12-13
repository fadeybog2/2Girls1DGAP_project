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
        self.onGround - переменная, отслеживающая нахождение на земле
        self.is_alive - жив ли?
        self.facing_right - куда смотрит персонаж
        self.hp - переменная, отслеживающая здоровье (хп, hp)

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
        self.is_alive = True
        self.facing_right = False
        self.hp = 5

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
            self.facing_right = False

        if right:
            self.vx = MOVE_SPEED  # движение вправо
            self.image = transform.flip(self.image0, True, False)
            self.facing_right = True

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
        Функция взаимодействия с платформами и врагами (vibe check)

        vx: скорость по горизонтали
        vy: скорость по вертикали
        platforms: список платформ
        """
        for p in platforms:
            if sprite.collide_rect(self, p):
                # проверка столкновения с платформой
                if isinstance(p, blocks.Spike):
                    # если пересакаемый блок - шипы
                    self.reborn()
                elif isinstance(p, mobs.Mob):
                    self.check_mob_hit(p)
                elif isinstance(p, blocks.Teleport):
                    self.teleporting(p.goX, p.goY)

                else:
                    if vx > 0:
                        self.rect.right = p.rect.left
                        self.vx = 0

                    if vx < 0:
                        self.rect.left = p.rect.right
                        self.vx = 0

                    if vy > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True  # теперь он на земле
                        self.vy = 0

                    if vy < 0:
                        self.rect.top = p.rect.bottom  # не может пробить платформу
                        self.vy = 0

    def check_mob_hit(self, mob):
        """
        Функция проверяет тип столкновения с мобом

        mob - объект класса Mob
        """
        vector_x = mob.rect.center[0] - self.rect.center[0]
        vector_y = mob.rect.center[1] - self.rect.center[1]
        # проверяем не прыгнули ли на моба сверху (да-да, как в марио)
        if abs(vector_x) <= (self.width + mob.width) / 2 and vector_y >= 0:
            self.vy *= -1  # отталкиваемся от моба
            self.rect.y += self.vy
            mob.hp -= 3  # понижаем хп моба
        else:
            self.reborn()  # иначе сами теряем хп

    def teleporting(self, goX, goY):
        """
        Функция телепортирования

        goX - координата x места назначения
        goY - координата y места назначения
        """
        self.rect.x = goX
        self.rect.y = goY
        
    def reborn(self):
        """
        Функция возрождения

        Если жизни еще остались - возрождается, если нет - умирает и endscreen
        """
        self.hp -= 1
        if self.hp == 0:  # умер совсем
            self.die()
        else:
            self.vx = 0
            self.vy = 0
            time.wait(500)
            self.teleporting(self.startX, self.startY)
            # перемещаемся в начальные координаты

    def die(self):
        self.is_alive = False
