import pygame as pg
from player import *
from blocks import *
from mobs import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
BLACK = (0, 0, 0)
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
    l = max(-(camera.width - SCREEN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - SCREEN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Bowling4life")
    surf = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Поверхность для рисования
    surf.fill(BLACK)
    bg = pg.image.load("background.jpg")  # background
    bg_width = bg.get_rect().size[0] * SCREEN_WIDTH // SCREEN_HEIGHT
    bg = pg.transform.scale(bg, [bg_width, SCREEN_HEIGHT])
    bg_rect = bg.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
    screen.blit(bg, bg_rect)

    hero = Player(55, 55)  # создаем героя по выбраным координатам
    left = right = False 
    up = False

    entities = pg.sprite.Group()  # Все рисуемые объекты
    mobs = pg.sprite.Group()  # Все движущиеся объекты
    platforms = []

    entities.add(hero)
    monster = Mob(200, 684, 1, 90)
    entities.add(monster)
    mobs.add(monster)
    platforms.append(monster)

    tp = Teleport(128, 512, 800, 64)
    sp = Spike(600, 684)
    entities.add(tp, sp)
    platforms.append(tp)
    platforms.append(sp)

    level = [
        "----------------------------------",
        "-                                -",
        "-                       ---      -",
        "-                           -    -",
        "-       -----                    -",
        "-                  --          - -",
        "--                               -",
        "-                            --- -",
        "-                 ----           -",
        "-     --                         -",
        "-                                -",
        "--                               -",
        "-                                -",
        "-                                -",
        "- ---                            -",
        "-                                -",
        "-                                -",
        "-   ------          ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-            ---                 -",
        "-                                -",
        "----------------------------------"]

    clock = pg.time.Clock()
    x = y = 0
    """
    читаем уровень, определяем координат платформ
    """
    for row in level:
        for symbol in row:
            if symbol == "-":
                platform = Platform(x, y)
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

    camera = Camera(camera_configure, level_width, level_height)
    finished = False
    while not finished:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == QUIT:
                finished = True
            if event.type == KEYDOWN and event.key == K_SPACE:
                up = True
            if event.type == KEYDOWN and event.key == K_a:
                left = True
            if event.type == KEYDOWN and event.key == K_d:
                right = True
            if event.type == KEYUP and event.key == K_SPACE:
                up = False
            if event.type == KEYUP and event.key == K_d:
                right = False
            if event.type == KEYUP and event.key == K_a:
                left = False

        screen.blit(bg, bg_rect)
        camera.update(hero)  # центровка камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        mobs.update(platforms)
        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))

        pg.display.update()


if __name__ == "__main__":
    main()
    pg.quit()
