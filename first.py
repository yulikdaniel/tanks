import pygame, sys, time
from pygame.locals import *
import play1, play2, play3, play4


class Bullet:
    def __init__(self, x, y, speed, direc, hit):
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
        self.height = 7
        self.width = 7

    def move(self):
        if not self.moved:
            if self.direction in ['up', 'down']:
                self.x -= 3
                if self.direction == 'up':
                    self.y -= 20
                else:
                    self.y += 20
            else:
                self.y -= 3
                if self.direction == 'left':
                    self.x -= 20
                else:
                    self.x += 20
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
        DISPLAYSURF.blit(self.appear, (self.x, self.y))

    def infield(self):
        return 0 <= self.x <= A and 0 <= self.y <= B


class Player:
    def __init__(self, x, y, app, direc, rt, fbul, liv, sm, wid, heig, name, sp, code):
        self.x, self.y = x, y
        self.rx, self.ry = x + 10, y
        self.appear = app
        self.direction = direc
        self.r_time = rt
        self.lives = liv
        self.m_life = liv
        self.type = 'Player'
        self.s_moment = sm
        self.width, self.height = wid, heig
        self.speed = sp
        self.last = [x, y]
        self.bullets = fbul
        self.name = name
        self.code = code

    def act(self, bullets):
        res = self.code()
        if res[0]:
            self.y -= self.speed
            self.direction = 'up'
        elif res[1]:
            self.y += self.speed
            self.direction = 'down'
        elif res[2]:
            self.x -= self.speed
            self.direction = 'left'
        elif res[3]:
            self.x += self.speed
            self.direction = 'right'
        if res[4] and time.time() - self.s_moment >= self.r_time and self.bullets:
            self.bullets -= 1
            self.shoot(bullets)
            self.s_moment = time.time()

    def upd(self):
        self.last = [self.x, self.y]
        exec('self.appear = ' + self.direction[0].upper() + '_TANK_IMG')

    def shoot(self, bullets):
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
        DISPLAYSURF.blit(self.appear, (self.x, self.y))
        text = font.render(str(self.bullets), True, (0, 128, 0))
        DISPLAYSURF.blit(text, (self.x - text.get_width() - 5, self.y))
        text2 = font.render(self.name, True, (0, 128, 0))
        DISPLAYSURF.blit(text2, (self.x, self.y + self.height))
        for x in range(self.lives):
            DISPLAYSURF.blit(HEART_IMG, (self.x + (20 - 10 * self.lives) + x * 20, self.y - 20))


A, B = 1850, 1000
FPS = 60
pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption('Tanks')
pygame.display.set_icon(pygame.image.load('Pics/tank2.png'))
DISPLAYSURF = pygame.display.set_mode((A, B))
font = pygame.font.SysFont("comicsansms", 20)
gifs = []

RELOAD_TIME = 0.7
PENALTY = 0.25
MAX_LIFE = 5
SPEED = 5
FBUL = 200
HEIGHT, WIDTH = 50, 50

HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (20, 20))
B_HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (50, 50))
S_HEART_IMG = pygame.transform.scale(pygame.image.load('Pics/heart.png'), (5, 5))

L_TANK_IMG = pygame.transform.scale(pygame.image.load('Pics/tank2.png'), (WIDTH, HEIGHT))
R_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 180)
U_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 270)
D_TANK_IMG = pygame.transform.rotate(L_TANK_IMG, 90)

R_BULLET_IMG = pygame.transform.scale(pygame.image.load('Pics/bullet.png'), (7, 7))
U_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 90)
L_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 180)
D_BULLET_IMG = pygame.transform.rotate(R_BULLET_IMG, 270)


def collide(obj1, obj2):
    resx1 = max(obj1.x, obj2.x)
    resx2 = min(obj1.x + obj1.width, obj2.x + obj2.width)
    resy1 = max(obj1.y, obj2.y)
    resy2 = min(obj1.y + obj1.height, obj2.y + obj2.height)
    if resy2 > resy1 and resx2 > resx1:
        return True
    return False

player1 = Player(A - 3 * WIDTH, B - 3 * HEIGHT, L_TANK_IMG, 'left', RELOAD_TIME, FBUL, MAX_LIFE, 0, WIDTH, HEIGHT, 'tiger', SPEED, play1.main)
player2 = Player(2 * WIDTH, 2 * HEIGHT, R_TANK_IMG, 'right', RELOAD_TIME, FBUL, MAX_LIFE, 0, WIDTH, HEIGHT, 't34', SPEED, play2.main)
player3 = Player(2 * WIDTH, B - 3 * HEIGHT, R_TANK_IMG, 'right', RELOAD_TIME, FBUL, MAX_LIFE, 0, WIDTH, HEIGHT, 'panzer', SPEED, play3.main)
player4 = Player(A - 3 * WIDTH, 2 * HEIGHT, R_TANK_IMG, 'left', RELOAD_TIME, FBUL, MAX_LIFE, 0, WIDTH, HEIGHT, 'leichtracktor', SPEED, play4.main)

bullets = []
objects = [player1, player2, player3, player4]

# pygame.display.toggle_fullscreen()
num = 0
k = 500
n = False
while True:
    num += 1
    if num % k == 0 or n:
        DISPLAYSURF.fill([200, 200, 0])
    for x in range(len(gifs)):
        try:
            if len(gifs[x][0]) == 0:
                del gifs[x]
            else:
                im = pygame.transform.scale(pygame.image.load(gifs[x][0].pop()), gifs[x][2])
                DISPLAYSURF.blit(im, gifs[x][1])
        except:
            pass
    for obj1 in objects:
        obj1.x %= 1850
        obj1.y %= 1010
        obj1.act(bullets)
        for obj2 in objects:
            if obj1 is not obj2 and collide(obj1, obj2):
                obj1.back()
        obj1.upd()
        if num % k == 0 or n:
            obj1.draw()

    cnt = -1
    for bullet in bullets:
        cnt += 1
        bullet.move()
        if not bullet.infield():
            # bullet.x %= A
            # bullet.y %= B
            del bullets[cnt]
            cnt -= 1
            continue
        for object in objects:
            if collide(object, bullet):
                if object.hit(bullet.hit):
                    objects.remove(object)
                del bullets[cnt]
                cnt -= 1
                break
        if num % k == 0 or n:
            bullet.draw()
    if num % k == 0 or n:
        pygame.display.update()
    if n:
        FPSCLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if key[pygame.K_SPACE]:
            n = True
        else:
            n = False
