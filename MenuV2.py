from pygame.locals import *
from json import loads, dumps
import pygame
from sys import exit
import TankV301 as main
from sys import setrecursionlimit

setrecursionlimit(1000000)


def write(ar):
    string, a, coor = ar
    DISPLAYSURF.blit(font.render(string, True, a), coor)


def f0():
    global mcur
    mcur = 0


def f1():
    global mcur
    mcur = 1


def f2():
    global mcur
    mcur = 2


def f3():
    global mcur
    mcur = 3


def fp():
    global settings, option, options, text8, UPS
    if text8[0] == 'Powerups are Enabled':
        text8[0] = 'Powerups are Disabled'
        UPS = False
    else:
        text8[0] = 'Powerups are Enabled'
        UPS = True
    settings['pow'] = not settings['pow']
    export()


def fv(up):
    global settings
    settings['volume'] += [-1, 1][int(up)]
    if settings['volume'] < 0:
        settings['volume'] = 0
    elif settings['volume'] > 10:
        settings['volume'] = 10
    text9[0] = 'Volume level: {}'.format(settings['volume'])
    export()


def fmul(up):
    global settings
    settings['players'] += [-1, 1][int(up)]
    if settings['players'] < 1:
        settings['players'] = 1
    elif settings['players'] > 4:
        settings['players'] = 4
    text11[0] = 'Players number: {}'.format(settings['players'])
    export()


def export():
    global settings
    with open('conf.tank', 'w') as f:
        f.write(dumps(settings))


def imp():
    global settings
    with open('conf.tank', 'r') as f:
        settings = loads(f.read().strip())


def upd():
    global text11, text9, text8
    text11[0] = 'Players number: {}'.format(settings['players'])
    text9[0] = 'Volume level: {}'.format(settings['volume'])
    text8[0] = 'Powerups are {}'.format(['Disabled', 'Enabled'][int(settings['pow'])])


def go():
    main.setup()
    main.run(settings)
    setup()
    run()


def setup():
    global FPS, FPSCLOCK, DISPLAYSURF, font, cur, mcur, text, text1, text2, text3, text4, text5, text6, text7, text8
    global text9, text10, text11, options, menus, cur, settings
    imp()
    FPS = 40
    pygame.init()
    pygame.key.set_repeat(1, 200)
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tanks')
    pygame.display.set_icon(pygame.image.load('Pics/tank2.png'))
    A, B = 1000, 1000
    DISPLAYSURF = pygame.display.set_mode((A, B))

    font = pygame.font.SysFont("comicsansms", 40)
    text = ['Multiplayer', (128, 128, 0), [10, 10]]
    text2 = ['Solo', (128, 128, 0), [10, 100]]
    text3 = ['Options', (128, 128, 0), [10, 190]]
    text4 = ['Local', (0, 128, 0), [10, 10]]
    text5 = ['Online', (0, 128, 0), [10, 100]]
    text6 = ['Back', (0, 128, 0), [10, 190]]
    text7 = ["Sorry, We haven't created the solo game yet", (0, 128, 0), [10, 10]]
    text8 = ['Powerups are Enabled', (0, 128, 0), [10, 10]]
    text9 = ['Volume level: {}'.format(settings['volume']), (0, 128, 0), [10, 100]]
    text10 = ['Quit', (128, 128, 0), [10, 280]]
    text11 = ['Players number: {}'.format(settings['players']), (128, 128, 0), [10, 280]]
    upd()

    options1 = [[text, f1], [text2, f2], [text3, f3], [text10, exit]]
    options2 = [[text4, go], [text5, f0], [text6, f0]]
    options3 = [[text7, f0]]
    options4 = [[text8, fp], [text9, fv, 1], [text6, f0], [text11, fmul, 1]]
    cur = 0
    mcur = 0
    options = options1[:]
    menus = [options1, options2, options3, options4]


def run():
    global FPS, FPSCLOCK, DISPLAYSURF, font, cur, mcur, text, text1, text2, text3, text4, text5, text6, text7, text8
    global text9, text10, text11, options, menus, cur, settings
    while True:
        DISPLAYSURF.fill([255, 200, 0])
        cnt = -1
        for option in options:
            cnt += 1
            if cur == cnt:
                option[0][1] = (128, 0, 0)
            else:
                option[0][1] = (128, 128, 0)
            write(option[0])
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    cur -= 1
                    cur %= len(options)
                if event.key == pygame.K_DOWN:
                    cur += 1
                    cur %= len(options)
                if event.key == pygame.K_LEFT and len(options[cur]) == 3:
                    options[cur][1](False)
                if event.key == pygame.K_RIGHT and len(options[cur]) == 3:
                    options[cur][1](True)
                cur %= len(options)
                if event.key == pygame.K_RETURN:
                    try:
                        options[cur][1]()
                    except TypeError:
                        pass
                    options = menus[mcur]
                    cur = 0


setup()
run()
