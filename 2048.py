import os
import random


_BOARDSIZE = 15
_SPACE = 4

_xPos = -1
_yPos = -1
_curr = 1
_max = 1
_isFinGame = False
_isExit = False
_isOver2048 = False

board = [[0 for col in range(_BOARDSIZE)] for row in range(_BOARDSIZE)]


def init():
    global _BOARDSIZE
    clearConsole()
    print('게임 시작전, 판의 크기를 정해주세요.(정사각형, 추천: 4x4)')
    while True:
        _BOARDSIZE = input('숫자 하나를 입력해주세요(3~11): ')
        try: _BOARDSIZE = int(_BOARDSIZE)
        except:
            print('숫자가 아닙니다. 다시 입력해주세요.')
            continue
        if _BOARDSIZE in range(3, 12):
            break
        else:
            print('범위를 초과하였습니다. 다시 입력해주세요.')
    xPos = random.randint(0, _BOARDSIZE-1)
    yPos = random.randint(0, _BOARDSIZE-1)
    board[xPos][yPos] = 2

def clearConsole():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def printBoard():
    clearConsole()
    print('2048 with Python ver 1115 (',str(_BOARDSIZE), 'x', str(_BOARDSIZE), ')')
    print('조작: WASD, 신규생성숫자: *, 현재 점수: ', _curr, ', 현재 최고점수(숫자): ', end='')
    if _curr == _max:
        print('*', end='')
    print(_max)
    print()
    for x in range(_BOARDSIZE):
        for y in range(_BOARDSIZE):
            if x == _xPos and y == _yPos:
                print('*'+ str(board[x][y]), ' '*(_SPACE-len(str(board[x][y]))), end='')
            elif board[x][y] == 0:
                print('■', ' '*(_SPACE-len(str(board[x][y]))), end='')
            else: print(board[x][y], ' '*(_SPACE-len(str(board[x][y]))+1), end='')
        for z in range(_SPACE-1):
            print()

def clearBoard():
    global _curr
    global _isFinGame
    _isFinGame = False
    _curr = 1
    for x in range(_BOARDSIZE):
        for y in range(_BOARDSIZE):
            board[x][y] = 0

def updateScore():
    global _max
    if _curr > _max:
        _max = _curr
    if _curr == 2048 and not _isOver2048:
        over2048()

def genNumRandomly():
    global _xPos
    global _yPos
    if hasNoSpace():
        _xPos = -1
        _yPos = -1
        return
    global _curr
    arg = random.randint(1, 5)
    while True:
        xPos = random.randint(0, _BOARDSIZE-1)
        yPos = random.randint(0, _BOARDSIZE-1)
        if board[xPos][yPos] == 0:
            if arg < 5:
                board[xPos][yPos] = 2
            else:
                board[xPos][yPos] = 4
            _xPos = xPos
            _yPos = yPos
            if board[xPos][yPos] > _curr:
                _curr = board[xPos][yPos]
            return

def checkDirAvailable(x, y, dir):
    if dir == 'Up':
        if x > 0: return True
        else: return False
    elif dir == 'Left':
        if y > 0: return True
        else: return False
    elif dir == 'Down':
        if x < _BOARDSIZE: return True
        else: return False
    elif dir == 'Right':
        if y < _BOARDSIZE: return True
        else: return False
    else: return False

def isPlayAvailable():
    global _isFinGame
    if _isFinGame:
        return False
    elif not hasNoSpace():
        return True
    for m in range(_BOARDSIZE-1, 0, -1):
            for n in range(0, _BOARDSIZE):
                    if board[m-1][n] == 0:
                        board[m-1][n] = board[m][n]
                        board[m][n] = 0
    for m in range(0, _BOARDSIZE-1):
        for n in range(0, _BOARDSIZE):
            if board[m+1][n] == 0:
                board[m+1][n] = board[m][n]
                board[m][n] = 0
    for n in range(_BOARDSIZE-1, 0, -1):
        for m in range(0, _BOARDSIZE):
            if board[m][n-1] == 0:
                board[m][n-1] = board[m][n]
                board[m][n] = 0
    for n in range(0, _BOARDSIZE-1):
        for m in range(0, _BOARDSIZE):
            if board[m][n+1] == 0:
                board[m][n+1] = board[m][n]
                board[m][n] = 0
    if hasNoSpace():
        if board[0][0] == board[0][1] or board[0][0] == board[1][0]:
            return True
        if board[_BOARDSIZE-1][_BOARDSIZE-1] == board[_BOARDSIZE-1][_BOARDSIZE-2] or board[_BOARDSIZE-1][_BOARDSIZE-1] == board[_BOARDSIZE-2][_BOARDSIZE-1]:
            return True
        if board[0][_BOARDSIZE-1] == board[0][_BOARDSIZE-2] or board[0][_BOARDSIZE-1] == board[1][_BOARDSIZE-1]:
            return True
        if board[_BOARDSIZE-1][0] == board[_BOARDSIZE-2][0] or board[_BOARDSIZE-1][0] == board[_BOARDSIZE-1][1]:
            return True
        for x in range(1, _BOARDSIZE-1):
            for y in range(1, _BOARDSIZE-1):
                if board[x][y] == board[x+1][y] or board[x][y] == board[x][y+1] or board[x][y] == board[x-1][y] or board[x][y] == board[x][y-1]:
                    return True
        _isFinGame = True
        return False
    else: return True

def hasNoSpace():
    for x in range(_BOARDSIZE):
        for y in range(_BOARDSIZE):
            if board[x][y] == 0:
                return False
    return True

def over2048():
    global _isFinGame
    global _isOver2048
    clearConsole()
    while True:
        print('2048 점을 넘으셨습니다!! 계속 플레이 하시겠습니까?')
        ovr = input('예: Y, 아니오: N: ')
        if ovr in ('Y', 'y', 'ㅇ'):
            _isOver2048 = True
            return
        elif ovr in ('N', 'n', 'ㄴ'):
            _isFinGame = True
            return
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
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
        print('잘못 입력하셨습니다. 다시 입력해주세요.')
        getInput()

def applyDir(_dir):
    global _curr
    if _dir == 'Up':
        for x in range(1, _BOARDSIZE, 1):
            for y in range(0, _BOARDSIZE):
                if checkDirAvailable(x, y, _dir):
                        for m in range(_BOARDSIZE-1, 0, -1):
                            for n in range(0, _BOARDSIZE):
                                if board[m-1][n] == 0:
                                    board[m-1][n] = board[m][n]
                                    board[m][n] = 0
                if board[x-1][y] == board[x][y]:
                    board[x-1][y] *= 2
                    board[x][y] = 0
                    if board[x-1][y] > _curr:
                        _curr = board[x-1][y]
    elif _dir == 'Left':
        for y in range(1, _BOARDSIZE, 1):
            for x in range(0, _BOARDSIZE):
                if checkDirAvailable(x, y, _dir):
                        for n in range(_BOARDSIZE-1, 0, -1):
                            for m in range(0, _BOARDSIZE):
                                if board[m][n-1] == 0:
                                    board[m][n-1] = board[m][n]
                                    board[m][n] = 0
                if board[x][y-1] == board[x][y]:
                    board[x][y-1] *= 2
                    board[x][y] = 0
                    if board[x][y-1] > _curr:
                        _curr = board[x][y-1]
    elif _dir == 'Down':
        for x in range(_BOARDSIZE-1, 0, -1):
            for y in range(0, _BOARDSIZE):
                if checkDirAvailable(x, y, _dir):
                        for m in range(0, _BOARDSIZE-1):
                            for n in range(0, _BOARDSIZE):
                                if board[m+1][n] == 0:
                                    board[m+1][n] = board[m][n]
                                    board[m][n] = 0
                if board[x][y] == board[x-1][y]:
                    board[x][y] *= 2
                    board[x-1][y] = 0
                    if board[x][y] > _curr:
                        _curr = board[x][y]
    elif _dir == 'Right':
        for y in range(_BOARDSIZE-1, 0, -1):
            for x in range(0, _BOARDSIZE):
                if checkDirAvailable(x, y, _dir):
                        for n in range(0, _BOARDSIZE-1):
                            for m in range(0, _BOARDSIZE):
                                if board[m][n+1] == 0:
                                    board[m][n+1] = board[m][n]
                                    board[m][n] = 0
                if board[x][y] == board[x][y-1]:
                    board[x][y] *= 2
                    board[x][y-1] = 0
                    if board[x][y] > _curr:
                        _curr = board[x][y]
    else: return

def _inGame():
    init()
    while not _isFinGame:
        genNumRandomly()
        updateScore()
        if not isPlayAvailable():
            break
        printBoard()
        getInput()
        print()

def inGame():
    global _isExit
    while not _isExit:
        _inGame()
        printBoard()
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
        clearBoard()
    print('게임을 종료하겠습니다. 최고점수: ', _max)
    input()


inGame()
