from random import randint

dir = 0


def main():
    global dir
    res = [0, 0, 0, 0, 0]
    if dir == 0:
        if randint(1, 3) == 1:
            dir = randint(1, 4)
            res[dir - 1] = 1
    else:
        if randint(1, 10) == 1:
            dir = randint(0, 4)
        if dir != 0:
            res[dir - 1] = 1
    if randint(1, 20) == 1:
        res[-1] = 1
    return res
