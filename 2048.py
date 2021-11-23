import os
import random


_BOARDSIZE = 4
_SPACE = 4
_MAXBOARDSIZE = 11

_xPos = -1
_yPos = -1
_curr = 1
_max = 1
_icon = 0
_version = 1121
_isOnGame = False
_isFinGame = False
_isExit = False
_isOver2048 = False

board = [[0 for col in range(_MAXBOARDSIZE)] for row in range(_MAXBOARDSIZE)]
icons = ['■', '□', '◆', '◇', '●', '○', '★', '☆']

def init():
    global _BOARDSIZE
    global _isFinGame
    global _isOnGame
    global _isExit
    readSettings()
    while True:
        clearConsole()
        print('2048 with Python ver', _version)
        print('1. Play  2. 설정 변경  3. Exit')
        ans = input('무엇을 하시겠습니까? ')
        try: ans = int(ans)
        except:
            print('숫자가 아닙니다. 다시 입력해주세요.')
            continue
        if ans == 1:
            _isOnGame = True
            break
        elif ans == 2:
            updateSettings()
        elif ans == 3:
            _isFinGame = True
            _isExit = True
            _BOARDSIZE = 1
            return
    clearConsole()
    xPos = random.randint(0, _BOARDSIZE-1)
    yPos = random.randint(0, _BOARDSIZE-1)
    board[xPos][yPos] = 2

def readSettings():
    global _max
    global _icon
    try:
        with open('data.bin', 'r') as file:
            lines = file.readlines()
            _max = int(lines[0])
            _icon = int(lines[1])
    except: return

def writeSettings():
    with open('data.bin', 'w') as file:
        file.write(str(_max) + '\n')
        file.write(str(_icon) + '\n')

def updateSettings():
    global _BOARDSIZE
    global _icon
    while True:
        clearConsole()
        print('1. 공백 아이콘 변경  2. 판 크기 변경  3. 나가기')
        ans = input('무엇을 하시겠습니까? ')
        try: ans = int(ans)
        except:
            print('숫자가 아닙니다. 다시 입력해주세요.')
            continue
        if ans == 1:
            while True:
                print('1. ■, 2. □, 3. ◆, 4. ◇, 5. ●, 6. ○, 7. ★, 8. ☆')
                print('현재 설정: ', end='')
                print(_icon+1)
                inp = input('무엇으로 하시겠습니까? ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if inp not in range(1, len(icons)+1):
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                _icon = inp-1
                print('완료하였습니다. 계속하시려면 아무 키나 눌러주세요.')
                input()
                break
        elif ans == 2:
            while True:
                print('판의 크기를 정해주세요.(정사각형, 추천: 4x4)')
                print('현재 판의 크기: ', end='')
                print(_BOARDSIZE)
                if not _isOnGame:
                    inp = input('숫자 하나를 입력해주세요(' + str(3) + '~' + str(_MAXBOARDSIZE) + '): ')
                else:
                    inp = input('숫자 하나를 입력해주세요(' + str(_BOARDSIZE) + '~' + str(_MAXBOARDSIZE) + '): ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if _isOnGame and inp < _BOARDSIZE:
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                elif inp in range(3, _MAXBOARDSIZE+1):
                    _BOARDSIZE = inp
                    print('완료하였습니다. 계속하시려면 아무 키나 눌러주세요.')
                    input()
                    break
                else:
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
        elif ans == 3:
            break
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
    writeSettings()

def clearConsole():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def printBoard():
    clearConsole()
    print('2048 with Python ver', _version, ' (',str(_BOARDSIZE), 'x', str(_BOARDSIZE), ')')
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
                print(icons[_icon], ' '*(_SPACE-len(str(board[x][y]))), end='')
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
    global _curr
    if hasNoSpace():
        _xPos = -1
        _yPos = -1
        return
    arg = random.randint(1, 10)
    while True:
        xPos = random.randint(0, _BOARDSIZE-1)
        yPos = random.randint(0, _BOARDSIZE-1)
        if board[xPos][yPos] == 0:
            if arg < 9:
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
    global _isFinGame
    key = input('방향: ')
    if key in ('W', 'w', 'ㅉ', 'ㅈ'):
        applyDir('Up')
    elif key in ('A', 'a', 'ㅁ'):
        applyDir('Left')
    elif key in ('S', 's', 'ㄴ'):
        applyDir('Down')
    elif key in ('D', 'd', 'ㅇ'):
        applyDir('Right')
    elif key in ('Z', 'z'):
        _isFinGame = True
    elif key in ('U', 'u'):
        updateSettings()
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
        writeSettings()
        while True:
            print('게임이 종료되었습니다. 다시하시겠습니까?')
            ans = input('다시시작: Y, 게임종료: N: ')
            if ans in ('Y', 'y', 'ㅇ'):
                _isOnGame = False
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
