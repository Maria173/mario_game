import os
import pygame
import random
import sys

pygame.init()

FPS = 100
WIDTH = 800
HEIGHT = 374
STEP = 10
TILE_WIDTH = TILE_HEIGHT = 34
JUMP_POWER = 10
MOVE_SPEED = 7
GRAVITY = 0.4
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
                  "       If you want to begin:",
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
        "-                        #                                                  -",
        "-                       --                                                  -",
        "-             x                                                 ---         -",
        "-     @      --                     x                                       -",
        "-     --             #              ------                                  -",
        "--                   ---                                                  ---",
        "-                                                       x                F  -",
        "-                                                       --               -  -",
        "-                                                                           -",
        "-----------------------------------------------------------------------------"]
level2 = [
<<<<<<< HEAD
        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "-                                                                           ------------",
        "-                                                                           ------------",
        "-   ----       x        --           x                                      ------------",
        "- @         -------            -----------                      ---       F ------------",
        "---                                             ----                     ---------------",
        "-                                                       x                   ------------",
        "-                                                       -----               ------------",
        "-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo------------",
        "----------------------------------------------------------------------------------------"]


platforms = [] # то, во что мы будем врезаться
obstacles = [] # то, из-за чего мы можем проиграть
finish = []    # здесь хранится флаг
cllctd_obj = [] # собираемые объекты

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                pf = Tile('wall', x, y)
                platforms.append(pf)
            elif level[y][x] == 'x':
                ob = Tile('obstacle', x, y)
                obstacles.append(ob)
            elif level[y][x] == 'o':
                ob = Tile('fire', x, y)
                obstacles.append(ob)
            elif level[y][x] == 'F':
                fg = Tile('flag', x, y)
                finish.append(fg)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '#':
                drg = Drugs('coin', x, y, 5, 2)
                cllctd_obj.append(drg)

    return new_player


tile_images = {'wall': load_image('mario_block.png'),
               'player': load_image('mario.png'),
               'obstacle': load_image('blackhole.png'),
               'fire': load_image('fire.png'),
               'flag': load_image('flag.png'),
               'coin': load_image('coin1.png')}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)

class Drugs(pygame.sprite.Sprite):
    cntr = 0
    def __init__(self, tile_type, pos_x, pos_y, columns, rows):
        super().__init__(tiles_group, all_sprites)

        self.frames = []
        self.cut_sheet(tile_images[tile_type], columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.rect.move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0,
                                sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i,
                                  self.rect.h * j)
                self.frames.append(sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size)
                ))

    def update(self):
        if Drugs.cntr % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        Drugs.cntr = (Drugs.cntr + 1) % 5

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

    def update(self, left, right, up, platforms, obstacles, finish, cllctd_obj):

        for ob in obstacles:    # если мы натыкаемся на препятствие, то мы проиграли, игра заканчивается
            if pygame.sprite.collide_rect(self, ob):
                self.kill()
                print('You lost!')
                terminate()

        for fg in finish:   # если мы достикли флаг, то мы выиграли, игра заканчивается
            if pygame.sprite.collide_rect(self, fg):
                print('You won!')
                terminate()
        for drg in cllctd_obj:
            if pygame.sprite.collide_rect(self, drg):
                drg.kill()

        if up:
            if self.onGround:  # прыгаем, только когда на земле
                self.yvel = -JUMP_POWER

        if left:
            self.xvel = -MOVE_SPEED  # влево = x - n


        if right:
            self.xvel = MOVE_SPEED  # вправо = x + n


        if not (left or right):
            self.xvel = 0


        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)



    def collide(self, xvel, yvel, platforms):

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # не движется влево

                if yvel > 0:  # если движется вниз
                    self.rect.bottom = p.rect.top  # не падает вниз
                    self.onGround = True  # тановится на блок
                    self.yvel = 0

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # не движется вверх
                    self.yvel = 0


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        # obj.rect.y += self.dy

    def update(self, target):
        if target.rect.x >= WIDTH // 2:
            self.dx = -(target.rect.x - WIDTH // 2)

        # self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)



start_screen()
player = generate_level(level2)
camera = Camera()


left = right = False  # по умолчанию - стоим
up = False
running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            up = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True

        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False

    screen.fill(pygame.Color(BACKGROUND_COLOR))
    tiles_group.draw(screen)
    player_group.draw(screen)
    camera.update(player)
    tiles_group.update()

    for sprite in all_sprites:
        camera.apply(sprite)

    player.update(left, right, up, platforms, obstacles, finish, cllctd_obj)
    pygame.display.flip()

terminate()
