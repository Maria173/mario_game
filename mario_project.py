import os
import pygame
import random
import sys

pygame.init()

FPS = 10
WIDTH = 800
HEIGHT = 374
STEP = 10
TILE_WIDTH = TILE_HEIGHT = 34
BACKGROUND_COLOR = "#228B22"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["             Super Mario",
                  "",
                  "       If you want to begin",
                  "            press any key ",
                  "        or tap the window"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT + 50))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# def load_level(filename):
#     filename = 'data/' + filename
#     with open(filename, 'r') as map_file:
#         level_map = [line.strip() for line in map_file]
#
#     max_width = max(map(len, level_map))
#     return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level1 = [
        "-----------------------------------------------------------------------------",
        "-                                                                           -",
        "-                       --                                                  -",
        "-                                                              ---          -",
        "-     @       -                                                             -",
        "-     --                            ------                                  -",
        "--                   ---                                                 ----",
        "-                                                                           -",
        "-                                                       --                  -",
        "-                                                                           -",
        "-----------------------------------------------------------------------------"]
level2 = [
        "-----------------------------------------------------------------------------",
        "-                                                                           -",
        "-                       --                                                  -",
        "-                                                              ---          -",
        "-     --                                                                    -",
        "- @                                 ------                                  -",
        "--                                                                       ----",
        "-                                                                           -",
        "-                                                       --                  -",
        "-                                                                           -",
        "-----------------------------------------------------------------------------"]


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)

    return new_player


tile_images = {'wall': load_image('mario_block.png'),
               'player': load_image('mario.png')}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15,
                                               TILE_HEIGHT * pos_y + 5)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        # obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        # self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
player = generate_level(level2)
camera = Camera()

running = True
pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_UP:  # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = True
        elif event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_UP:  # up arrow goes up
                pressed_up = False
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = False

    # In your game loop, check for key states:
    if pressed_left:
        player.rect.x -= STEP
    if pressed_right:
        player.rect.x += STEP
    if pressed_up:
        player.rect.y -= STEP
    if pressed_down:
        player.rect.y += STEP

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(BACKGROUND_COLOR))
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
terminate()

