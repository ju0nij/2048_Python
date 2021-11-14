import os
import random


_MAPSIZE = 15
_SPACE = 4

_newX = -1
_newY = -1
_curr = 1
_max = 1
_isFinished = False
_isExit = False
_isOver2048 = False

map = [[0 for col in range(_MAPSIZE)] for row in range(_MAPSIZE)]


def init():
    global _MAPSIZE
    clearConsole()
    print('게임 시작전, 판의 크기를 정해주세요.(정사각형, 추천: 4x4)')
    while True:
        _MAPSIZE = input('숫자 하나를 입력해주세요(3~11): ')
        try: _MAPSIZE = int(_MAPSIZE)
        except:
            print('숫자가 아닙니다. 다시 시도해주세요.')
            continue
        if _MAPSIZE in range(3, 12):
            break
        else:
            print('범위를 초과하였습니다. 다시 입력해주세요.')
    xpos = random.randint(0, _MAPSIZE-1)
    ypos = random.randint(0, _MAPSIZE-1)
    map[xpos][ypos] = 2

def clearConsole():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def printMap():
    clearConsole()
    print('2048 with Python ver 1114 (',str(_MAPSIZE), 'x', str(_MAPSIZE), ')')
    print('조작: WASD, 신규생성숫자: *, 현재 점수: ', _curr, ', 현재 최고점수(숫자): ', end='')
    if _curr == _max:
        print('*', end='')
    print(_max)
    print()
    for x in range(_MAPSIZE):
        for y in range(_MAPSIZE):
            if x == _newX and y == _newY:
                print('*'+ str(map[x][y]), ' '*(_SPACE-len(str(map[x][y]))), end='')
            elif map[x][y] == 0:
                print('■', ' '*(_SPACE-len(str(map[x][y]))), end='')
            else: print(map[x][y], ' '*(_SPACE-len(str(map[x][y]))+1), end='')
        for z in range(_SPACE-1):
            print()

def clearMap():
    global _curr
    global _isFinished
    _isFinished = False
    _curr = 1
    for x in range(_MAPSIZE):
        for y in range(_MAPSIZE):
            map[x][y] = 0

def updateScore():
    global _max
    if _curr > _max:
        _max = _curr
    if _curr == 2048 and not _isOver2048:
        over2048()

def makeItRandomly():
    global _newX
    global _newY
    if hasNoSpace():
        _newX = -1
        _newY = -1
        return
    global _curr
    arg = random.randint(1, 5)
    while True:
        xpos = random.randint(0, _MAPSIZE-1)
        ypos = random.randint(0, _MAPSIZE-1)
        if map[xpos][ypos] == 0:
            if arg < 5:
                map[xpos][ypos] = 2
            else:
                map[xpos][ypos] = 4
            _newX = xpos
            _newY = ypos
            if map[xpos][ypos] > _curr:
                _curr = map[xpos][ypos]
            return

def checkAvailableDir(x, y, dir):
    if dir == 'Up':
        if x > 0: return True
        else: return False
    elif dir == 'Left':
        if y > 0: return True
        else: return False
    elif dir == 'Down':
        if x < _MAPSIZE: return True
        else: return False
    elif dir == 'Right':
        if y < _MAPSIZE: return True
        else: return False
    else: return False

def isPlayAvailable():
    global _isFinished
    if _isFinished:
        return False
    elif not hasNoSpace():
        return True
    for m in range(_MAPSIZE-1, 0, -1):
            for n in range(0, _MAPSIZE):
                    if map[m-1][n] == 0:
                        map[m-1][n] = map[m][n]
                        map[m][n] = 0
    for m in range(0, _MAPSIZE-1):
        for n in range(0, _MAPSIZE):
            if map[m+1][n] == 0:
                map[m+1][n] = map[m][n]
                map[m][n] = 0
    for n in range(_MAPSIZE-1, 0, -1):
        for m in range(0, _MAPSIZE):
            if map[m][n-1] == 0:
                map[m][n-1] = map[m][n]
                map[m][n] = 0
    for n in range(0, _MAPSIZE-1):
        for m in range(0, _MAPSIZE):
            if map[m][n+1] == 0:
                map[m][n+1] = map[m][n]
                map[m][n] = 0
    if hasNoSpace():
        if map[0][0] == map[0][1] or map[0][0] == map[1][0]:
            return True
        if map[_MAPSIZE-1][_MAPSIZE-1] == map[_MAPSIZE-1][_MAPSIZE-2] or map[_MAPSIZE-1][_MAPSIZE-1] == map[_MAPSIZE-2][_MAPSIZE-1]:
            return True
        if map[0][_MAPSIZE-1] == map[0][_MAPSIZE-2] or map[0][_MAPSIZE-1] == map[1][_MAPSIZE-1]:
            return True
        if map[_MAPSIZE-1][0] == map[_MAPSIZE-2][0] or map[_MAPSIZE-1][0] == map[_MAPSIZE-1][1]:
            return True
        for x in range(1, _MAPSIZE-1):
            for y in range(1, _MAPSIZE-1):
                if map[x][y] == map[x+1][y] or map[x][y] == map[x][y+1] or map[x][y] == map[x-1][y] or map[x][y] == map[x][y-1]:
                    return True
        _isFinished = True
        return False
    else: return True

def hasNoSpace():
    for x in range(_MAPSIZE):
        for y in range(_MAPSIZE):
            if map[x][y] == 0:
                return False
    return True

def over2048():
    global _isFinished
    global _isOver2048
    clearConsole()
    while True:
        print('2048 점을 넘으셨습니다!! 계속 플레이 하시겠습니까?')
        ovr = input('예: Y, 아니오: N: ')
        if ovr in ('Y', 'y', 'ㅇ'):
            _isOver2048 = True
            return
        elif ovr in ('N', 'n', 'ㄴ'):
            _isFinished = True
            return
        else:
            print('잘못 입력하셨습니다. 다시 시도해주세요.')
            continue

def getInput():
    key = input('방향: ')
    if key in ('W', 'w', 'ㅉ', 'ㅈ'):
        applyDir('Up')
    elif key in ('A', 'a', 'ㅁ'):
        applyDir('Left')
    elif key in ('S', 's', 'ㄴ'):
        applyDir('Down')
    elif key in ('D', 'd', 'ㅇ'):
        applyDir('Right')
    else:
        print('잘못 입력하셨습니다. 다시 시도해주세요.')
        getInput()

def applyDir(_dir):
    global _curr
    if _dir == 'Up':
        for x in range(1, _MAPSIZE, 1):
            for y in range(0, _MAPSIZE):
                if checkAvailableDir(x, y, _dir):
                        for m in range(_MAPSIZE-1, 0, -1):
                            for n in range(0, _MAPSIZE):
                                if map[m-1][n] == 0:
                                    map[m-1][n] = map[m][n]
                                    map[m][n] = 0
                if map[x-1][y] == map[x][y]:
                    map[x-1][y] *= 2
                    map[x][y] = 0
                    if map[x-1][y] > _curr:
                        _curr = map[x-1][y]
    elif _dir == 'Left':
        for y in range(1, _MAPSIZE, 1):
            for x in range(0, _MAPSIZE):
                if checkAvailableDir(x, y, _dir):
                        for n in range(_MAPSIZE-1, 0, -1):
                            for m in range(0, _MAPSIZE):
                                if map[m][n-1] == 0:
                                    map[m][n-1] = map[m][n]
                                    map[m][n] = 0
                if map[x][y-1] == map[x][y]:
                    map[x][y-1] *= 2
                    map[x][y] = 0
                    if map[x][y-1] > _curr:
                        _curr = map[x][y-1]
    elif _dir == 'Down':
        for x in range(_MAPSIZE-1, 0, -1):
            for y in range(0, _MAPSIZE):
                if checkAvailableDir(x, y, _dir):
                        for m in range(0, _MAPSIZE-1):
                            for n in range(0, _MAPSIZE):
                                if map[m+1][n] == 0:
                                    map[m+1][n] = map[m][n]
                                    map[m][n] = 0
                if map[x][y] == map[x-1][y]:
                    map[x][y] *= 2
                    map[x-1][y] = 0
                    if map[x][y] > _curr:
                        _curr = map[x][y]
    elif _dir == 'Right':
        for y in range(_MAPSIZE-1, 0, -1):
            for x in range(0, _MAPSIZE):
                if checkAvailableDir(x, y, _dir):
                        for n in range(0, _MAPSIZE-1):
                            for m in range(0, _MAPSIZE):
                                if map[m][n+1] == 0:
                                    map[m][n+1] = map[m][n]
                                    map[m][n] = 0
                if map[x][y] == map[x][y-1]:
                    map[x][y] *= 2
                    map[x][y-1] = 0
                    if map[x][y] > _curr:
                        _curr = map[x][y]
    else: return

def _inGame():
    init()
    while not _isFinished:
        makeItRandomly()
        updateScore()
        if not isPlayAvailable():
            break
        printMap()
        getInput()
        print()

def inGame():
    global _isExit
    while not _isExit:
        _inGame()
        printMap()
        while True:
            print('게임이 종료되었습니다. 다시하시겠습니까?')
            ans = input('다시시작: Y, 게임종료: N: ')
            if ans in ('Y', 'y', 'ㅇ'):
                break
            elif ans in ('N', 'n', 'ㄴ'):
                _isExit = True
                break
            else:
                print('잘못 입력하셨습니다. 다시 입력해주세요.')
                continue
        clearMap()
    print('게임을 종료하겠습니다. 최고점수: ', _max)
    input()


inGame()
