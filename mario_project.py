import os
import pygame
# import random
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

while True:
    level = input('Level number (1, 2, 3, 4 or 5) : ')
    if level in ['1', '2', '3', '4', '5']:
        break
    else:
        print('There is no such level! Try again')

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coll_obj_group = pygame.sprite.Group()


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


def start_screen(level_n):
    need_str = "       You chose level " + str(level_n)
    intro_text = ["           Super Mario",
                  "",
                  need_str,
                  "      If you want to begin:",
                  "           press any key ",
                  "       or tap the window"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT + 50))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 15
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


level1 = [

        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "-                                                                      #    ------------",
        "-                         x             ----            x             ---   ------------",
        "- @               -----------                           -----               ------------",
        "---                                                 x                       ------------",
        "-         --                 #     --           #   -----        --------   ------------",
        "-   #          #            -----               -                          F------------",
        "------         -                                                           -------------",
        "-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo------------",
        "----------------------------------------------------------------------------------------"]

level2 = [

        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "-                     #                     #       #                       ------------",
        "-                    --                    ---     ---                      ------------",
        "-   ----       x        --           x                                      ------------",
        "- @         -------            -----------                      ---       F ------------",
        "---      #                 #                    ----                     ---------------",
        "-       --                 ---                          x              #    ------------",
        "-                                                       -----          -    ------------",
        "-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo------------",
        "----------------------------------------------------------------------------------------"]
        
level3 = [

        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "- @                              #                       #                  ------------",
        "--------                        --                       -          #x      ------------",
        "-                  x         --                    x               ----     ------------",
        "-                ----                         --------          --          ------------",
        "-    #                                 ----                              F  ------------",
        "-   ---                ---                          #                -----  ------------",
        "-         -----                                    --------                 ------------",
        "-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo------------",
        "----------------------------------------------------------------------------------------"]

level4 = [

        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "-                                                      #                   #------------",
        "-           x     --                                   --         ----     -------------",
        "-           ---                        x        ---             x           ------------",
        "-                 #            -----   -              #      ----           ------------",
        "-     ----        -                                  --                   F ------------",
        "-  @                  ----            #    ----                          ---------------",
        "-  -                                 --                                     ------------",
        "-ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo------------",
        "----------------------------------------------------------------------------------------"]

level5 = [

        "----------------------------------------------------------------------------------------",
        "-                                                                           ------------",
        "-                #                                                X         ------------",
        "-                -                                             -----        ------------",
        "-  #   x                                         x                      #x  ------------",
        "-  --  ---                           -----      --                     ---  ------------",
        "-                          x   #                   #        ----            ------------",
        "-           -----      -   -   -                   --                       ------------",
        "-@                                                                         F------------",
        "--ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-------------",
        "----------------------------------------------------------------------------------------"]

platforms = []  # то, во что мы будем врезаться
obstacles = []  # то, из-за чего мы можем проиграть
finish = []    # здесь хранится флаг
cllctd_obj = []  # собираемые объекты


def generate_level(what_level):
    new_player, x, y = None, None, None
    for y in range(len(what_level)):
        for x in range(len(what_level[y])):
            if what_level[y][x] == '-':
                pf = Tile('wall', x, y)
                platforms.append(pf)
            elif what_level[y][x] == 'x':
                ob = Tile('obstacle', x, y)
                obstacles.append(ob)
            elif what_level[y][x] == 'o':
                ob = Tile('fire', x, y)
                obstacles.append(ob)
            elif what_level[y][x] == 'F':
                fg = Tile('flag', x, y)
                finish.append(fg)
            elif what_level[y][x] == '@':
                new_player = Player(x, y)
            elif what_level[y][x] == '#':
                drg = Drugs('coin', x, y, 5, 2)
                cllctd_obj.append(drg)

    return new_player


tile_images = {'wall': load_image('mario_block.png'),
               'player': load_image('mario.png'),
               'obstacle': load_image('blackhole.png'),
               'fire': load_image('fire.png'),
               'flag': load_image('flag.png'),
               'coin': load_image('coin.png')}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


class Drugs(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, columns, rows):
        super().__init__(coll_obj_group, all_sprites)

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

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False

    def update(self, left_d, right_d, up_d, platforms_list, obstacles_list, finish_list, cllctd_obj_list):
        for ob in obstacles_list:    # если мы натыкаемся на препятствие, то мы проиграли, игра заканчивается
            if pygame.sprite.collide_rect(self, ob):
                self.kill()
                print('You lost!')
                terminate()

        for fg in finish_list:   # если мы достикли флаг, то мы выиграли, игра заканчивается
            if pygame.sprite.collide_rect(self, fg):
                print('You won!')
                terminate()
        for drg in cllctd_obj_list:
            if pygame.sprite.collide_rect(self, drg):
                drg.kill()

        if up_d:
            if self.onGround:  # прыгаем, только когда на земле
                self.yvel = -JUMP_POWER

        if left_d:
            self.xvel = -MOVE_SPEED  # влево = x - n

        if right_d:
            self.xvel = MOVE_SPEED  # вправо = x + n

        if not (left_d or right_d):
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms_list)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms_list)

    def collide(self, x_vel, y_vel, platforms_list):

        for p in platforms_list:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if x_vel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # не движется вправо

                if x_vel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # не движется влево

                if y_vel > 0:  # если движется вниз
                    self.rect.bottom = p.rect.top  # не падает вниз
                    self.onGround = True  # тановится на блок
                    self.yvel = 0

                if y_vel < 0:  # если движется вверх
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


if level == '1':
    start_screen(1)
    player = generate_level(level1)
if level == '2':
    start_screen(2)
    player = generate_level(level2)
if level == '3':
    start_screen(3)
    player = generate_level(level3)
if level == '4':
    start_screen(4)
    player = generate_level(level4)
if level == '5':
    start_screen(5)
    player = generate_level(level5)

camera = Camera()

cntr = 0
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
    coll_obj_group.draw(screen)
    camera.update(player)

    if cntr % 5 == 0:
        coll_obj_group.update()
    cntr = (cntr + 1) % 5

    for sprite in all_sprites:
        camera.apply(sprite)

    player.update(left, right, up, platforms, obstacles, finish, cllctd_obj)
    pygame.display.flip()

terminate()
