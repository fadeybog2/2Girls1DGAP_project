import pygame as pg
from player import *
from blocks import *
from mobs import *
from menu import *
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
BLACK = (0, 0, 0)
MAROON = (128, 0, 0)
WHITE = (255, 255, 255)
FPS = 60


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + SCREEN_WIDTH / 2, -t + SCREEN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - SCREEN_WIDTH),
            l)  # Не движемся дальше правой границы
    t = max(-(camera.height - SCREEN_HEIGHT),
            t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def spawn_fireball(player):
    """
    Функция спавнит fireball в зависимости от направления, куда смотрит игрок

    player: объект класса player

    Возвращает объект класса Fireball
    """
    if player.facing_right:
        ball = Fireball(player.rect.right, player.rect.center[1])
    else:
        ball = Fireball(player.rect.left, player.rect.center[1])
        ball.flip_velocity()
    return ball


def spawn_new_thing(class0, platforms, free_platforms, area=0, goX=0, goY=0):
    """
    Функция спавнит нового моба, шип или телепорт рандомно на свободные
    платформы

    platforms: список платформ
    free_platforms: количество свободных для спавна платформ
    class0: объект какого класса мы спавним, можно Mob, Spike или Teleport
    area: max длина перемещения моба
    goX, goY - координаты назначения телепорта

    Возвращает объект класса class0
    """
    number = randint(2, free_platforms)
    i = 0
    done = False
    if free_platforms != 0:
        for p in platforms:
            if p.is_free:
                i += 1
                if i == number:
                    x, y = p.rect.topleft[0], p.rect.topleft[1]
                    if class0 == Mob:
                        thing = Mob(x, y, area)
                    elif class0 == Spike:
                        thing = Spike(x, y)
                    elif class0 == Teleport:
                        thing = Teleport(x, y, goX, goY)
                    done = True
                    free_platforms -= 1
    if done:
        return thing
    else:
        return 1


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Bowling4life")
    surf = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Поверхность для рисования
    surf.fill(BLACK)
    play = Button(screen, 380, 250, BLACK, 'play!')
    rules = Button(screen, 380, 300, BLACK, 'rules')
    quit = Button(screen, 350, 560, BLACK, 'quit')  # кнопка руководства
    buttons = [play, rules]  # список кнопок меню
    ls = pg.image.load("Zastavka.jpg")  # фон меню
    bg = pg.image.load("background.jpg")  # background
    bg_width = bg.get_rect().size[0] * SCREEN_WIDTH // SCREEN_HEIGHT
    bg = pg.transform.scale(bg, [bg_width, SCREEN_HEIGHT])
    bg_rect = bg.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    health = pg.image.load("heart.png")  # изображение hp
    health_x, health_y = 35, 30  # коорд. topleft первого сердца
    life = pg.image.load("live.png")  # изображение жизней (шары)
    life_x, life_y = 65, 0  # topleft первого мяча

    hero = Player(55, 55)  # создаем героя по выбраным координатам
    up = attacking = False
    gameplay = False  # идет ли игра
    started = True  # запустили ли игру только что
    manual = False  # открыты ли правила

    entities = pg.sprite.Group()  # Все рисуемые объекты
    mobs = pg.sprite.Group()  # Все движущиеся объекты
    balls = pg.sprite.Group()  # Все летящие снаряды
    platforms = []
    free_platforms = 0  # кол-во свободных для спавна платформ

    # Читаем файлик с уровнем
    f = open('level.txt', 'r')
    level = [line.strip() for line in f]

    x = y = 0
    """
    читаем уровень, определяем координат платформ
    """
    for row in level:
        for symbol in row:
            if symbol == "-":  # обычная платформа
                platform = Platform(x, y)
                entities.add(platform)
                platforms.append(platform)
                free_platforms += 1

            elif symbol == "1":  # платформа с шипом
                # последняя добавленная платформа
                last_p = platforms[len(platforms) - 1]
                # если пол
                if isinstance(last_p, blocks.Wall) and last_p.is_free:
                    platform = Wall(x, y)
                else:
                    platform = Platform(x, y)
                    platform.is_free = False
                spike = Spike(x, y)
                entities.add(spike)
                platforms.append(spike)

            elif symbol == "=":  # стена
                platform = Wall(x, y)

            elif symbol == "+":  # пол
                platform = Wall(x, y)
                platform.is_free = True
                free_platforms += 1

            entities.add(platform)
            platforms.append(platform)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0  # обнуление x для последующих строк

    """
    определяем размеры уровня с учетом границ
    """
    level_width = len(level[0]) * PLATFORM_WIDTH
    level_height = len(level) * PLATFORM_HEIGHT

    # создаем телепорт (рандомно)
    tp = spawn_new_thing(Teleport, platforms, free_platforms, 0, 900, 64)
    entities.add(tp)
    platforms.append(tp)

    entities.add(hero)
    for i in range(0, 3):
        monster = spawn_new_thing(Mob, platforms, free_platforms, 10)
        entities.add(monster)
        mobs.add(monster)
        platforms.append(monster)

    clock = pg.time.Clock()

    camera = Camera(camera_configure, level_width, level_height)
    finished = False
    while not finished:
        clock.tick(FPS)
        left = right = False
        if pg.key.get_pressed()[pg.K_a]:
            left = True
        if pg.key.get_pressed()[pg.K_d]:
            right = True
        for event in pg.event.get():
            if event.type == QUIT:
                finished = True
            if event.type == KEYDOWN and event.key == K_w:
                up = True
            if event.type == KEYUP and event.key == K_w:
                up = False
            if event.type == KEYDOWN and event.key == K_LALT:
                ball = spawn_fireball(hero)
                balls.add(ball)
                entities.add(ball)
                hero.attacking = True
                hero.time_attack = 0

        if not hero.is_alive:
            screen.fill(BLACK)
            font = pg.font.Font(None, 120)
            text = font.render("YOU DIED", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2,
                                              SCREEN_HEIGHT // 2))
            gameplay = False
            screen.blit(text, text_rect)

        else:
            if started:
                # если началась игра, то включается стартовый экран
                start_screen(screen, ls, SCREEN_WIDTH, SCREEN_HEIGHT, buttons)
                # проверка нажатия кнопочек
                for event in pg.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        (x_hit, y_hit) = event.pos
                        play.hitting(x_hit, y_hit)
                        rules.hitting(x_hit, y_hit)
                        if play.click:
                            # закрываем меню, начинаем игру
                            started, gameplay = False, True
                        if rules.click:
                            # закрываем меню, открываем правила
                            started, manual = False, True
            if manual:
                # если тыкнули на правила, то рисуем правила
                manual_draw(screen, ls, SCREEN_WIDTH, SCREEN_HEIGHT, quit)
                # Чекаем, попали ли по кнопке выход
                for event in pg.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        (x_hit, y_hit) = event.pos
                        quit.hitting(x_hit, y_hit)
                        if quit.click:
                            # если попали, то закрываем мануал, открываем меню
                            started, manual = True, False
            if gameplay:
                # наконеч-то начинаем играть в боОоулинг
                screen.blit(bg, bg_rect)
                camera.update(hero)  # центровка камеру относительно персонажа
                hero.update(left, right, up, platforms, FPS)  # передвижение
                mobs.update(platforms, FPS)
                for mob in mobs:
                    if not mob.is_alive:
                        mob.kill()  # отсеивает мёртвые
                        mobs.remove(mob)
                        platforms.remove(mob)
                        free_platforms += 1
                        enemy = spawn_new_thing(Mob, platforms, free_platforms,
                                                10)
                        if not type(enemy) == int:
                            entities.add(enemy)
                            mobs.add(enemy)
                            platforms.append(enemy)
                for ball in balls:
                    if not ball.is_alive:
                        ball.kill()  # отсеивает мёртвые
                    ball.move(mobs, platforms)
                for entity in entities:
                    screen.blit(entity.image, camera.apply(entity))
                # циклы отрисовки HP и жизней
                for i in range(hero.hp):
                    hp_rect = health.get_rect(topleft=[health_x + 35 * i,
                                                       health_y])
                    screen.blit(health, hp_rect)
                for i in range(hero.lives):
                    lf_rect = life.get_rect(topleft=[life_x + 35 * i,
                                                           life_y])
                    screen.blit(life, lf_rect)
                # Подписываем, где что
                font = pg.font.Font(None, 30)
                text = font.render("Lives:", True, WHITE)
                text_rect = text.get_rect(topleft = (0, 5))
                screen.blit(text, text_rect)
                text1 = font.render("HP:", True, WHITE)
                text_rect1 = text.get_rect(topleft=(0, 39))
                screen.blit(text1, text_rect1)

        pg.display.update()


if __name__ == "__main__":
    main()
    pg.quit()
