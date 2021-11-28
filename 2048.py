import os
import random

_version = 1125

class Pos:
    def __init__(self, size):
        self.__xpos = 0
        self.__ypos = 0
        self.__arg = 0
        self.genNumRandomly(size)
        
    def isNew(self, x, y):
        if x == self.xpos and y == self.ypos:
            return True
        else: return False
        
    def setPos(self, x, y):
        self.__xpos = x
        self.__ypos = y
        
    def genNumRandomly(self, size):
        num = random.randint(1, 10)
        self.__xpos = random.randint(0, size-1)
        self.__ypos = random.randint(0, size-1)
        if num < 9: self.__arg = 2
        else: self.__arg = 4
        
    def getX(self):
        return self.__xpos
    
    def getY(self):
        return self.__ypos
    
    def getValue(self):
        return self.__arg
    
class G2048:
    def __init__(self, boardsize, maxboardsize, icon, _max):
        self._boardsize = boardsize
        self._maxboardsize = maxboardsize
        self._icon = icon
        self._max = _max
        self.BOARD = [[0 for col in range(self._maxboardsize+1)] for row in range(self._maxboardsize+1)]
        self.ICONS = ['■', '□', '◆', '◇', '●', '○', '★', '☆']
        self._isOnGame = False
        self._isFinGame = False
        self._isExit = False
        self._isOver2048 = False
        self._curr = 1
        self._space = 4
        self._NUMBER = Pos(self._boardsize)
        
    def setData(self, max, icon, boardsize):
        self._max = max
        self._boardsize = boardsize
        self._icon = icon

    def setBoardData(self, x, y, data):
        self.BOARD[x][y] = data
    
    def getBoardData(self, x, y):
        return self.BOARD[x][y]
    
    def printBoard(self):
        clearConsole()
        print('2048 with Python ver', _version, ' (',str(self._boardsize), 'x', str(self._boardsize), ')')
        print('조작: WASD, 신규생성숫자: *, 설정: U, 게임 종료: Z')
        print('현재 점수: ', self._curr, ', 현재 최고점수(숫자): ', end='')
        if self._curr == self._max:
            print('*', end='')
        print(self._max)
        print()
        for x in range(self._boardsize):
            for y in range(self._boardsize):
                if x == self._NUMBER.getX() and y == self._NUMBER.getY():
                    print('*'+ str(self.getBoardData(x,y)), ' '*(self._space-len(str(self.getBoardData(x,y)))), end='')
                elif self.getBoardData(x,y) == 0:
                    print(self.ICONS[self._icon], ' '*(self._space-len(str(self.getBoardData(x,y)))), end='')
                else: print(self.getBoardData(x,y), ' '*(self._space-len(str(self.getBoardData(x,y)))+1), end='')
            for z in range(self._space-1):
                print()
                
    def clearBoard(self):
        self._isFinGame = False
        self._curr = 1
        for x in range(self._boardsize):
            for y in range(self._boardsize):
                self.setBoardData(x,y,0)
                
    def updateScore(self):
        if self._curr > self._max:
            self._max = self._curr
            
    def checkDirAvailable(self, x, y, dir):
        if dir == 'Up':
            if x > 0: return True
            else: return False
        elif dir == 'Left':
            if y > 0: return True
            else: return False
        elif dir == 'Down':
            if x < self._boardsize: return True
            else: return False
        elif dir == 'Right':
            if y < self._boardsize: return True
            else: return False
        else: return False
        
    def hasNoSpace(self):
        for x in range(self._boardsize):
            for y in range(self._boardsize):
                if self.BOARD[x][y] == 0:
                    return False
        return True

    def applyDir(self, _dir):
        if _dir == 'Up':
            for x in range(1, self._boardsize, 1):
                for y in range(0, self._boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for m in range(self._boardsize-1, 0, -1):
                            for n in range(0, self._boardsize):
                                if self.getBoardData(m-1,n) == 0:
                                    self.setBoardData(m-1,n,self.getBoardData(m,n))
                                    self.setBoardData(m,n,0)
                    if self.getBoardData(x-1,y) == self.getBoardData(x,y):
                        self.setBoardData(x-1,y, self.getBoardData(x-1,y)*2)
                        self.setBoardData(x,y,0)
                        if self.getBoardData(x-1,y) > self._curr:
                            self._curr = self.getBoardData(x-1,y)
        elif _dir == 'Left':
            for y in range(1, self._boardsize, 1):
                for x in range(0, self._boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for n in range(self._boardsize-1, 0, -1):
                            for m in range(0, self._boardsize):
                                if self.BOARD[m][n-1] == 0:
                                    self.BOARD[m][n-1] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y-1] == self.BOARD[x][y]:
                        self.BOARD[x][y-1] *= 2
                        self.BOARD[x][y] = 0
                        if self.BOARD[x][y-1] > self._curr:
                            self._curr = self.BOARD[x][y-1]
        elif _dir == 'Down':
            for x in range(self._boardsize-1, 0, -1):
                for y in range(0, self._boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for m in range(0, self._boardsize-1):
                            for n in range(0, self._boardsize):
                                if self.BOARD[m+1][n] == 0:
                                    self.BOARD[m+1][n] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y] == self.BOARD[x-1][y]:
                        self.BOARD[x][y] *= 2
                        self.BOARD[x-1][y] = 0
                        if self.BOARD[x][y] > self._curr:
                            self._curr = self.BOARD[x][y]
        elif _dir == 'Right':
            for y in range(self._boardsize-1, 0, -1):
                for x in range(0, self._boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for n in range(0, self._boardsize-1):
                            for m in range(0, self._boardsize):
                                if self.BOARD[m][n+1] == 0:
                                    self.BOARD[m][n+1] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y] == self.BOARD[x][y-1]:
                        self.BOARD[x][y] *= 2
                        self.BOARD[x][y-1] = 0
                        if self.BOARD[x][y] > self._curr:
                            self._curr = self.BOARD[x][y]
        else: return
        
    def isPlayAvailable(self):
        if self._isFinGame:
            return False
        elif not self.hasNoSpace():
            return True
        for m in range(self._boardsize-1, 0, -1):
                for n in range(0, self._boardsize):
                        if self.BOARD[m-1][n] == 0:
                            self.BOARD[m-1][n] = self.BOARD[m][n]
                            self.BOARD[m][n] = 0
        for m in range(0, self._boardsize-1):
            for n in range(0, self._boardsize):
                if self.BOARD[m+1][n] == 0:
                    self.BOARD[m+1][n] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        for n in range(self._boardsize-1, 0, -1):
            for m in range(0, self._boardsize):
                if self.BOARD[m][n-1] == 0:
                    self.BOARD[m][n-1] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        for n in range(0, self._boardsize-1):
            for m in range(0, self._boardsize):
                if self.BOARD[m][n+1] == 0:
                    self.BOARD[m][n+1] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        if hasNoSpace():
            for x in range(0, self._boardsize):
                for y in range(0, self._boardsize):
                    if self.BOARD[x][y] == self.BOARD[x+1][y] or self.BOARD[x][y] == self.BOARD[x][y+1] or self.BOARD[x][y] == self.BOARD[x-1][y] or self.BOARD[x][y] == self.BOARD[x][y-1]:
                        return True
            self._isFinGame = True
            return False
        else: return True
        
    def FinishGame(self):
        self._isFinGame = True
        self._isExit = True
        
    def genNum(self):
        if self.hasNoSpace():
            self._NUMBER.setPos(-1,-1)
            return
        while True:
            self._NUMBER.genNumRandomly(self._boardsize)
            if self.BOARD[self._NUMBER.getX()][self._NUMBER.getY()] == 0:
                self.BOARD[self._NUMBER.getX()][self._NUMBER.getY()] = self._NUMBER.getValue()
                if self.BOARD[self._NUMBER.getX()][self._NUMBER.getY()] > self._curr:
                    self._curr = self.BOARD[self._NUMBER.getX()][self._NUMBER.getY()]
                    self.updateScore()
                return

MAIN = G2048(4,11,0,1)
def init():
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
            MAIN._isOnGame = True
            MAIN.clearBoard()
            break
        elif ans == 2:
            updateSettings()
        elif ans == 3:
            Main.FinishGame()
            return
        else: continue
    clearConsole()
    xPos = random.randint(0, MAIN._boardsize-1)
    yPos = random.randint(0, MAIN._boardsize-1)
    MAIN.BOARD[xPos][yPos] = 2

def readSettings():
    try:
        with open('data.bin', 'r') as file:
            lines = file.readlines()
            try: _max = int(lines[0])
            except: _max = 1
            try: _icon = int(lines[1])
            except: _icon = 0
            try: _BOARDSIZE = int(lines[2])
            except: _BOARDSIZE = 4
    except: return
    if _max > 100000:
        _max = 1
    if _icon not in range(0, 8):
        _icon = 0
    if _BOARDSIZE not in range(3, MAIN._maxboardsize+1):
        _BOARDSIZE = 4
    MAIN.setData(_max, _icon, _BOARDSIZE)

def writeSettings():
    with open('data.bin', 'w') as file:
        file.write(str(MAIN._max) + '\n')
        file.write(str(MAIN._icon) + '\n')
        file.write(str(MAIN._boardsize) + '\n')

def updateSettings():
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
                print(MAIN._icon+1)
                inp = input('무엇으로 하시겠습니까? ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if inp not in range(1, len(MAIN.ICONS)+1):
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                MAIN._icon = inp-1
                print('완료하였습니다. 계속하시려면 아무 키나 눌러주세요.')
                input() 
                break
        elif ans == 2:
            while True:
                print('판의 크기를 정해주세요.(정사각형, 추천: 4x4)')
                print('현재 판의 크기: ', end='')
                print(MAIN._boardsize)
                if not MAIN._isOnGame:
                    inp = input('숫자 하나를 입력해주세요(' + str(3) + '~' + str(MAIN._maxboardsize) + '): ')
                else:
                    inp = input('숫자 하나를 입력해주세요(' + str(MAIN._boardsize) + '~' + str(MAIN._maxboardsize) + '): ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if MAIN._isOnGame and inp < MAIN._boardsize:
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                elif inp in range(3, MAIN._maxboardsize+1):
                    MAIN._boardsize = inp
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

def gameOver():
    if not MAIN._isExit:
        MAIN.printBoard()
    while not MAIN._isExit:
        print('게임이 종료되었습니다. 다시하시겠습니까?')
        ans = input('다시시작: Y, 게임종료: N: ')
        if ans in ('Y', 'y', 'ㅇ'):
            MAIN._isOnGame = False
            MAIN._isFinGame = False
            return
        elif ans in ('N', 'n', 'ㄴ'):
            break
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        MAIN.clearBoard()
        MAIN.printBoard()
    print('게임을 종료하겠습니다. ', end='')
    if not MAIN._isExit:
        MAIN._isExit = True
        print('최고점수: ', MAIN._max)
    input()

def getInput():
    key = input('방향: ')
    if key in ('W', 'w', 'ㅉ', 'ㅈ'):
        MAIN.applyDir('Up')
    elif key in ('A', 'a', 'ㅁ'):
        MAIN.applyDir('Left')
    elif key in ('S', 's', 'ㄴ'):
        MAIN.applyDir('Down')
    elif key in ('D', 'd', 'ㅇ'):
        MAIN.applyDir('Right')
    elif key in ('Z', 'z'):
        MAIN._isFinGame = True
    elif key in ('U', 'u'):
        updateSettings()
    else:
        print('잘못 입력하셨습니다. 다시 입력해주세요.')
        getInput()

def _inGame():
    init()
    while not MAIN._isFinGame:
        MAIN.genNum()
        if not MAIN.isPlayAvailable():
            break
        MAIN.printBoard()
        getInput()
        print()

def inGame():
    while not MAIN._isExit:
        _inGame()
        writeSettings()
        gameOver()

inGame()
