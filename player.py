import pygame as pg
import blocks
import mobs

MOVE_SPEED = 7
HEIGHT = 48
JUMP_POWER = 10
GRAVITY = 0.5
FIREBALL_VELOCITY = 10


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        """
        Конструктор класса Player

        self.vx, self.vy - скорость в проекции на горизонталь и вертикаль
        self.startX, self.startY = x, y - начальные координаты
        self.onGround - переменная, отслеживающая нахождение на земле
        self.is_alive - жив ли?

        переменные для анимации:
        self.facing_right - куда смотрит персонаж, type bool
        self.got_hit - получил ли урон недавно, type bool
        self.attacking - атакует ли, type bool
        self.time_hit - время с последнего получения урона
        self.time_attack - время с последней атаки
        self.time_shield - время щита

        self.shield - щит в момент сразу после получения урона
        self.hp - переменная, отслеживающая здоровье (хп, hp)
        self.lives - жизни
        self.score - счет

        self.teleporting_sound - звук при телепортации, загружается из файла 
        teleporting_sound.wav

        можно загрузить любой спрайт с названием hero.png и hero_scream.png, код
        сам отформатирует размер
        """
        pg.sprite.Sprite.__init__(self)
        self.images = [pg.image.load("hero.png"),  # норми
                       pg.image.load("hero_rage.png"),  # получает урон
                       pg.image.load("hero_scream.png"),  # атакует
                       pg.image.load("hero_rage_scream.png")]  # атакует&урон
        # форматируем размер
        self.height = HEIGHT
        for i in range(0, len(self.images)):
            hero_size = self.images[i].get_rect().size
            self.width = self.height * hero_size[0] // hero_size[1]
            self.images[i] = pg.transform.scale(self.images[i],
                                                [self.width, self.height])

        self.image = self.images[0]  # default
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = self.vy = 0
        self.startX, self.startY = x, y
        self.teleporting_sound = pg.mixer.Sound('teleporting_sound.wav')
        self.teleporting_sound.set_volume(0.1)
        self.onGround = False
        self.is_alive = True
        self.facing_right = False
        self.got_hit = False
        self.attacking = False
        self.shield = False

        self.time_hit = 0
        self.time_attack = 0
        self.time_shield = 0
        self.lives = 3
        self.hp = 5
        self.score = 0

    def update(self, left, right, up, platforms, fps):
        """
        Функция обработки нажатия клавиш

        left: управление движением влево
        right: управление движением вправо
        up: прыжок
        platforms: список платформ
        attacking: переменная, отслеживающая атаку
        """
        if up:
            if self.onGround:
                # двойной прыжок не прописан, прыгает только с земли
                self.vy = -JUMP_POWER

        if left:
            self.vx = -MOVE_SPEED  # движение влево
            self.facing_right = False

        if right:
            self.vx = MOVE_SPEED  # движение вправо
            self.facing_right = True

        if not (left or right):  # стоит чиллит
            self.vx = 0

        if not self.onGround:
            # изменение скорости в прыжке
            self.vy += GRAVITY

        self.change_image(fps)

        self.onGround = False
        self.rect.y += self.vy
        self.bump(0, self.vy, platforms, fps)

        self.rect.x += self.vx  # движение игрока на Vx
        self.bump(self.vx, 0, platforms, fps)

    def change_image(self, fps):
        """
        Функция определяет какую картинку нужно выводить в зависимости от
        активности героя

        FPS: фпс - частота кадров
        """
        attack = hit = 0
        self.picture_changed(self.images[0])
        if self.got_hit:
            self.time_hit += 1
            if 1 <= self.time_hit < 2 * fps // 3:
                hit = 2
            elif self.time_hit == 2 * fps // 3:
                hit = 0
                self.time_hit = 0
                self.got_hit = False
        if self.attacking:
            self.time_attack += 1
            if 1 <= self.time_attack < fps // 3:
                attack = 2
            elif self.time_attack == fps // 3:
                self.time_attack = 0
                self.attacking = False
        if attack * hit == 4:
            self.picture_changed(self.images[3])
        elif attack == 2:
            self.picture_changed(self.images[2])
        elif hit == 2:
            self.picture_changed(self.images[1])

    def picture_changed(self, image):
        """
        Функция меняет картинку на заданную

        image: картинка, на которую меняем
        """
        self.image = image
        # куда смотрит персонаж
        if self.facing_right:
            self.image = pg.transform.flip(image, True, False)
        else:
            self.image = image

    def bump(self, vx, vy, platforms, fps):
        """
        Функция взаимодействия с платформами и врагами (vibe check)

        vx: скорость по горизонтали
        vy: скорость по вертикали
        platforms: список платформ
        """
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                # проверка столкновения с платформой
                if isinstance(p, blocks.Spike):
                    # если пересакаемый блок - шипы
                    self.got_hit = True
                    self.time_hit = 0
                    self.reborn()
                elif isinstance(p, mobs.Mob):
                    self.check_mob_hit(p, fps)
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

    def check_mob_hit(self, mob, fps):
        """
        Функция проверяет тип столкновения с мобом

        mob - объект класса Mob
        """
        vector_x = mob.rect.center[0] - self.rect.center[0]
        vector_y = mob.rect.center[1] - self.rect.bottom
        # проверяем не прыгнули ли на моба сверху (да-да, как в марио)
        if abs(vector_x) <= (self.width + mob.width) / 2 and vector_y >= 0:
            self.vy = -2 * JUMP_POWER // 3  # отталкиваемся от моба
            self.rect.y += self.vy
            mob.hp -= 3  # понижаем хп моба
            mob.got_hit = True  # для анимации
        else:
            self.got_hit = True
            self.time_hit = 0
            self.get_damage(fps)  # иначе сами теряем хп
            self.shield = True

    def teleporting(self, goX, goY):
        """
        Функция телепортирования

        goX - координата x места назначения
        goY - координата y места назначения
        """
        self.vx = 0
        self.vy = 0
        self.rect.x = goX
        self.rect.y = goY
        self.teleporting_sound.play()

    def get_damage(self, fps):
        """
        Функция получения урона (уменьшения здоровья)

        fps - частота кадров

        Если осталось здороровье - ничего; не осталось - респавнится
        """
        if self.shield:
            self.time_shield += 1
            if self.time_shield == fps:
                self.shield = False
                self.time_shield = 0
        if not self.shield:
            self.hp -= 1
        if self.hp == 0:  # умер
            self.reborn()

    def reborn(self):
        """
        Функция возрождения

        Если жизни еще остались - возрождается, если нет - умирает и endscreen
        """
        self.lives -= 1
        if self.lives == 0:  # умер совсем
            self.die()
        else:
            self.vx = 0
            self.vy = 0
            self.hp = 5
            pg.time.wait(500)
            self.teleporting(self.startX, self.startY)
            # перемещаемся в начальные координаты

    def die(self):
        """
        Функция смерти
        """
        self.is_alive = False
        self.score = 0


class Fireball(pg.sprite.Sprite):
    """
    Конструктор класса Fireball

    self.vx - скорость в проекции на горизонталь (по вертикали нельзя - фича)
    x, y - начальные координаты
    self.is_alive - жив ли?
    """

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("fireball.png")
        self.rad = 12
        self.image = pg.transform.scale(self.image,
                                        [self.rad * 2, self.rad * 2])
        self.rect = self.image.get_rect(center=(x, y))
        self.is_alive = True
        self.vx = FIREBALL_VELOCITY

    def check_walls(self, platforms):
        """
        Функция взаимодействия с платформами (vibe check)

        platforms: список платформ и стен
        """
        for p in platforms:
            if pg.sprite.collide_rect(self, p):
                # проверка столкновения с платформой
                if not isinstance(p, mobs.Mob) or \
                        not isinstance(p, Player):
                    # если не моб или игрок
                    self.is_alive = False

    def flip_velocity(self):
        self.vx *= -1

    def move(self, mobs, platforms):
        self.rect.x += self.vx
        self.hit_check(mobs)
        self.check_walls(platforms)

    def hit_check(self, mobs):
        """
        Функция взаимодействия с мобами (vibe check)

        mobs: список мобов
        """
        # FIXME почему-то один fireball снижает 2 hp за раз ???
        for m in mobs:
            if pg.sprite.collide_rect(self, m):
                # проверка столкновения с мобом
                m.hp -= 1
                m.got_hit = True  # для анимации
                self.is_alive = False
