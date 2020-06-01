import pygame, sys, time
from pygame.locals import *
from random import randint


class PowerUp:
    def __init__(self, type, x, y):
        self.type = type
        self.x, self.y = x, y
        self.width, self.height = 50, 50
        if self.type == 'heart':
            self.appear = B_HEART_IMG
        elif self.type == 'ammo':
            self.appear = AMMO_IMG
        elif self.type == 'mgun':
            self.appear = GUN_IMG
        elif self.type == 'shield':
            self.appear = SHIELD_IMG
        elif self.type == 'acc':
            self.appear = ACC_IMG
        elif self.type == 'fireball':
            self.appear = FIRE_IMG

    def effect(self, player):
        ef = lambda x: x
        if self.type == 'heart':
            player.lives += 1
            player.lives = min(player.lives, MAX_LIFE)
        elif self.type == 'ammo':
            player.bullets += 30
        else:
            if self.type == 'mgun':
                def ef(ob):
                    ob.r_time = RELOAD_TIME

                player.r_time = 0.15
            elif self.type == 'shield':
                def ef(ob):
                    ob.DEST = True

                player.DEST = False
            elif self.type == 'acc':
                def ef(ob):
                    ob.speed = SPEED

                player.speed = 15
            if player.effects[self.type] is None:
                player.effects[self.type] = [ef, time.time() + 15]
            else:
                player.effects[self.type][1] += 15

    def draw(self):
        DISPLAYSURF.blit(self.appear, (self.x, self.y))


class Player:
    def __init__(self, x, y, app, direc, rt, liv, cont, sm, wid, heig, name, sp):
        self.x, self.y = x, y
        self.rx, self.ry = x + 10, y
        self.appear = app
        self.direction = direc
        self.r_time = rt
        self.lives = liv
        self.m_life = liv
        self.controls = cont
        self.type = 'Player'
        self.s_moment = sm
        self.width, self.height = wid, heig
        self.speed = sp
        self.DEST = True
        self.last = [x, y]
        self.bullets = FBUL
        self.name = name
        self.mat = True
        self.htbl = True
        self.effects = {'fireball': None, 'acc': None, 'mgun': None, 'shield': None}

    def upd(self):
        self.last = [self.x, self.y]
        for pup in self.effects.keys():
            if self.effects[pup] is not None:
                if self.effects[pup][1] <= time.time():
                    self.effects[pup][0](self)
                    self.effects[pup] = None

    def shoot(self, bullets):
        if self.effects['fireball'] is not None:
            bullets.append(Bullet(self.x + 25, self.y + 25, 20, self.direction, 2, True))
        else:
            bullets.append(Bullet(self.x + 25, self.y + 25, 20, self.direction, 1))

    def back(self):
        self.x, self.y = self.last

    def hit(self, l):
        self.lives -= l
        if self.lives <= 0:
            global gifs
            gifs.append([['Gif/exp/' + str(x) + '.png' for x in range(47)][::-1], (self.x - 25, self.y - 25), (90, 90)])
        return self.lives <= 0

    def draw(self):
        if not self.DEST:
            if self.direction == 'right':
                DISPLAYSURF.blit(INV_IMG, (self.x - 10, self.y - 6))
            elif self.direction == 'left':
                DISPLAYSURF.blit(INV_IMG, (self.x - 6, self.y - 8))
            elif self.direction == 'up':
                DISPLAYSURF.blit(INV_IMG, (self.x - 10, self.y - 6))
            else:
                DISPLAYSURF.blit(INV_IMG, (self.x - 10, self.y - 13))
        DISPLAYSURF.blit(self.appear, (self.x, self.y))
        text = font.render(str(self.bullets), True, (0, 128, 0))
        DISPLAYSURF.blit(text, (self.x - text.get_width() - 5, self.y))
        text2 = font.render(self.name, True, (0, 128, 0))
        DISPLAYSURF.blit(text2, (self.x, self.y + self.height))
        for x in range(self.lives):
            DISPLAYSURF.blit(HEART_IMG, (self.x + (20 - 10 * self.lives) + x * 20, self.y - 20))


class Thing:
    def __init__(self, x, y, width, height, des, mat, hittable, app=None):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.DEST = des
        self.mat = mat
        self.htbl = hittable
        self.type = 'thing'
        self.appear = None
        if app is not None:
            self.appear = app

    def hit(self, dmg):
        if self.appear == BLOCK3_IMG:
            return True
        elif dmg == 1:
            self.appear = BLOCK3_IMG
            self.x += 2.5
            self.y += 2.5
            return False
        else:
            return True

    def draw(self):
        if self.appear is not None:
            DISPLAYSURF.blit(self.appear, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, speed, direc, hit, fb=False):
        self.x, self.y = x, y
        self.speed = speed
        self.direction = direc
        self.hit = hit
        self.moved = False
        if self.direction == 'up':
            self.appear = U_BULLET_IMG
        elif self.direction == 'down':
            self.appear = D_BULLET_IMG
        elif self.direction == 'right':
            self.appear = R_BULLET_IMG
        else:
            self.appear = L_BULLET_IMG
        self.fb = fb
        if fb is not False:
            self.appear = FIREBALL_IMG
        self.height = 7
        self.width = 7
        if fb is not False:
            self.height = 15
            self.width = 15

    def move(self):
        if not self.moved:
            if self.direction in ['up', 'down']:
                self.x -= 3
                if self.direction == 'up':
                    self.y -= 20
                    if self.fb:
                        self.y -= 8
                else:
                    self.y += 20
                    if self.fb:
                        self.y += 8
            else:
                self.y -= 3
                if self.direction == 'left':
                    self.x -= 20
                    if self.fb:
                        self.x -= 8
                else:
                    self.x += 20
                    if self.fb:
                        self.x += 8
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed
        self.moved = True

    def draw(self):
        if self.fb:
            DISPLAYSURF.blit(self.appear, (self.x - 3.5, self.y - 3.5))
        else:
            DISPLAYSURF.blit(self.appear, (self.x, self.y))

    def infield(self):
        return 0 <= self.x <= A and 0 <= self.y <= B


def setup():
    global A, B, FPS, FPSCLOCK, DISPLAYSURF, font, gifs, field, UPS, PENALTY, FBUL, HEART_IMG, B_HEART_IMG
    global S_HEART_IMG, AMMO_IMG, GUN_IMG, SHIELD_IMG, INV_IMG, ACC_IMG, FIREBALL_IMG, FIRE_IMG, FOREST_IMG, WATER_IMG
    global BLOCK_IMG, BLOCK2_IMG, BLOCK3_IMG, player1, player2, player3, player4, L_TANK_IMG, R_TANK_IMG
    global U_TANK_IMG, D_TANK_IMG, L_BULLET_IMG, R_BULLET_IMG, U_BULLET_IMG, D_BULLET_IMG, MAX_LIFE, SPEED, RELOAD_TIME
    A, B = 1850, 1000
    FPS = 50
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tanks')
    pygame.display.set_icon(pygame.image.load('Pics/tank2.png'))
    DISPLAYSURF = pygame.display.set_mode((A, B))
    font = pygame.font.SysFont("comicsansms", 20)
    gifs = []

    with open('Maps/Map{}'.format(randint(1, 2)), 'r') as f1:
        field = [[int(y) for y in x.strip()] for x in f1.readlines()]

    UPS = True

    RELOAD_TIME = 0.7
    PENALTY = 0.25
    MAX_LIFE = 5
    SPEED = 5
    FBUL = 50
    HEIGHT, WIDTH = 50, 50

    HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (20, 20))
    B_HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (50, 50))
    S_HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (5, 5))

    AMMO_IMG = pygame.transform.scale(pygame.image.load('Pics/sup.png'), (50, 50))
    GUN_IMG = pygame.transform.scale(pygame.image.load('Pics/Gun.png'), (50, 50))
    SHIELD_IMG = pygame.transform.scale(pygame.image.load('Pics/Shield.png'), (50, 50))
    INV_IMG = pygame.transform.scale(pygame.image.load('Pics/Inv.png'), (65, 65))
    ACC_IMG = pygame.transform.scale(pygame.image.load('Pics/Acc.png'), (50, 50))
    FIREBALL_IMG = pygame.transform.scale(pygame.image.load('Pics/fire.png'), (20, 20))
    FIRE_IMG = pygame.transform.scale(pygame.image.load('Pics/fireball.jpeg'), (50, 50))

    FOREST_IMG = pygame.transform.scale(pygame.image.load('Pics/forest.jpg'), (50, 50))
    WATER_IMG = pygame.transform.scale(pygame.image.load('Pics/water.jpg'), (50, 50))
    BLOCK_IMG = pygame.transform.scale(pygame.image.load('Pics/block.jpg'), (50, 50))
    BLOCK2_IMG = pygame.transform.scale(pygame.image.load('Pics/block2.jpg'), (50, 50))
    BLOCK3_IMG = pygame.transform.scale(pygame.image.load('Pics/block3.jpg'), (45, 45))

    L_TANK_IMG = pygame.transform.scale(pygame.image.load('Pics/tank2.png'), (WIDTH, HEIGHT))
    R_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 180)
    U_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 270)
    D_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 90)

    R_BULLET_IMG = pygame.transform.scale(pygame.image.load('Pics/bullet.png'), (7, 7))
    U_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 90)
    L_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 180)
    D_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 270)

    player1 = Player(A - 3 * WIDTH, B - 3 * HEIGHT, L_TANK_IMG, 'left', RELOAD_TIME, MAX_LIFE,
                     [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL], 0, WIDTH, HEIGHT,
                     'Petka', SPEED)
    player2 = Player(2 * WIDTH, 2 * HEIGHT, R_TANK_IMG, 'right', RELOAD_TIME, MAX_LIFE,
                     [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_1], 0, WIDTH, HEIGHT, 'Yulik', SPEED)
    player3 = Player(A - 3 * WIDTH, 2 * HEIGHT, L_TANK_IMG, 'left', RELOAD_TIME, MAX_LIFE,
                     [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, pygame.K_SPACE], 0, WIDTH, HEIGHT, 'Warrior',
                     SPEED)
    player4 = Player(2 * WIDTH, B - 3 * HEIGHT, L_TANK_IMG, 'right', RELOAD_TIME, MAX_LIFE,
                     [pygame.K_z, pygame.K_LSUPER, pygame.K_LCTRL, pygame.K_LALT, pygame.K_LSHIFT], 0, WIDTH, HEIGHT,
                     'Loch', SPEED)


def collide(obj1, obj2):
    for x in [obj1.x, obj1.x + obj1.width]:
        for y in [obj1.y, obj1.y + obj1.height]:
            if obj2.x <= x <= obj2.x + obj2.width and obj2.y <= y <= obj2.y + obj2.height:
                return True
    for x in [obj2.x, obj2.x + obj2.width]:
        for y in [obj2.y, obj2.y + obj2.height]:
            if obj1.x <= x <= obj1.x + obj1.width and obj1.y <= y <= obj1.y + obj1.height:
                return True
    return False


def spawn():
    x, y = randint(0, 36), randint(0, 19)
    if field[y][x] == 0 or field[y][x] == 3:
        return x * 50, y * 50
    else:
        return spawn()


def run(settings):
    bullets = []
    objects = [player1, player2, player3, player4][:settings['players']]
    for y in range(B // 50):
        for x in range(A // 50):
            if field[y][x] == 1:
                objects.append(Thing(x * 50, y * 50, 50, 50, False, True, True, BLOCK_IMG))
            elif field[y][x] == 2:
                objects.append(Thing(x * 50, y * 50, 50, 50, True, True, True, BLOCK2_IMG))
            elif field[y][x] == 3:
                objects.append(Thing(x * 50, y * 50, 50, 50, False, False, False, FOREST_IMG))
            elif field[y][x] == 4:
                objects.append(Thing(x * 50, y * 50, 50, 50, False, True, False, WATER_IMG))
    if settings['pow']:
        ups = []
        difups = {'heart': 0, 'ammo': 0, 'powerup': 0}
    # pygame.display.toggle_fullscreen()
    while True:
        if sum([int(player1 in objects), int(player2 in objects), int(player3 in objects),
                int(player4 in objects)]) <= 1 and not gifs:
            return
        DISPLAYSURF.fill([50, 255, 50])
        DISPLAYSURF.fill((0, 0, 0))
        for x in range(len(gifs)):
            try:
                if len(gifs[x][0]) == 0:
                    del gifs[x]
                else:
                    im = pygame.transform.scale(pygame.image.load(gifs[x][0].pop()), gifs[x][2])
                    DISPLAYSURF.blit(im, gifs[x][1])
            except:
                pass
        for x in objects:
            x.x %= 1850
            x.y %= 1010
        if settings['pow']:
            x, y = spawn()
            if randint(1300, 1600) == 1543 and difups['powerup'] <= 3:
                ups.append(PowerUp(['acc', 'mgun', 'shield', 'fireball'][randint(0, 3)], x, y))
                difups['powerup'] += 1
            if randint(1300, 1600) == 1543 and difups['ammo'] == 0:
                ups.append(PowerUp('ammo', x, y))
                difups['ammo'] += 1
            if randint(1300, 1600) == 1543 and player1.lives + player2.lives + difups['heart'] < 2 * MAX_LIFE:
                difups['heart'] += 1
                ups.append(PowerUp('heart', x, y))
            cnt = -1
            for up in ups:
                cnt += 1
                up.draw()
                for object in objects:
                    if object.type == 'Player' and collide(object, up) and len(ups) > cnt:
                        del ups[cnt]
                        if up.type in ['heart', 'ammo']:
                            difups[up.type] -= 1
                        else:
                            difups['powerup'] -= 1
                        up.effect(object)

        key = pygame.key.get_pressed()
        for obj in objects:
            if obj.type == 'Player':
                odir = obj.direction
                exec("obj.appear = " + obj.direction[0].capitalize() + "_TANK_IMG")
                if key[obj.controls[0]]:
                    obj.y -= obj.speed
                    obj.direction = 'up'
                elif key[obj.controls[1]]:
                    obj.y += obj.speed
                    obj.direction = 'down'
                elif key[obj.controls[2]]:
                    obj.x -= obj.speed
                    obj.direction = 'left'
                elif key[obj.controls[3]]:
                    obj.x += obj.speed
                    obj.direction = 'right'
                for obj2 in objects:
                    if obj is not obj2:
                        if collide(obj, obj2) and obj.mat and obj2.mat:
                            obj.back()
                            break
                obj.upd()
                if obj.direction != odir:
                    obj.x, obj.y = obj.x + (obj.width - obj.height) // 2, obj.y + (obj.height - obj.width) // 2
                    obj.width, obj.height = obj.height, obj.width
                if key[obj.controls[4]] and time.time() - obj.s_moment >= obj.r_time and obj.bullets:
                    obj.bullets -= 1
                    obj.shoot(bullets)
                    obj.s_moment = time.time()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            return
        # if key[pygame.K_m]:
            # pygame.display.toggle_fullscreen()
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        for player in objects:
            if not (player.DEST == False and player.mat == False):
                player.draw()
        cnt = -1
        for bullet in bullets:
            cnt += 1
            bullet.move()
            if not bullet.infield():
                del bullets[cnt]
                cnt -= 1
                continue
            for object in objects:
                if collide(object, bullet):
                    if object.DEST:
                        if object.hit(bullet.hit):
                            objects.remove(object)
                    if object.type == "Player" and bullet.fb and object.effects['shield'] is not None:
                        object.DEST = True
                        object.effects['shield'] = None
                        del bullets[cnt]
                        cnt -= 1
                    else:
                        if object.htbl:
                            del bullets[cnt]
                            cnt -= 1		
                    break
            bullet.draw()
        for obj in objects:
            if obj.appear == FOREST_IMG:
                obj.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
