import os
import random

_version = 1125
_isExit = False

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
    def __init__(self, filename):
        lists = self.readSettings(filename)
        self.__max = lists[0]
        self.__icon = lists[1]
        self.__boardsize = lists[2]
        self.__maxboardsize = lists[3]
        self.BOARD = [[0 for col in range(self.__maxboardsize+1)] for row in range(self.__maxboardsize+1)]
        self.ICONS = ['■', '□', '◆', '◇', '●', '○', '★', '☆']
        self.__isOnGame = False
        self.__isFinGame = False
        self.__curr = 1
        self.__space = 4
        self.__NUMBER = Pos(self.__boardsize)
        
    def getData(self, var='null'):
        if var == 'null': return [self.__max, self.__icon, self.__boardsize, self.__maxboardsize]
        elif var == 'max': return self.__max
        elif var == 'icon': return self.__icon
        elif var == 'boardsize': return self.__boardsize
        elif var == 'maxboardsize': return self.__maxboardsize
        else: return null
        
    def setData(self, max='null', icon='null', boardsize='null'):
        if max != 'null': self.__max = max
        if icon != 'null': self.__icon = icon
        if boardsize != 'null': self.__boardsize = boardsize

    def setBoardData(self, x, y, data):
        self.BOARD[x][y] = data
    
    def getBoardData(self, x, y):
        return self.BOARD[x][y]

    def isOnGame(self, var='null'):
        if var == 'null': return self.__isOnGame
        else:
            self.__isOnGame = var
            return
        
    def isFinGame(self, var='null'):
        if var == 'null': return self.__isFinGame
        else:
            self.__isFinGame = var
            return
        
    def readSettings(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                try: _max = int(lines[0])
                except: _max = 1
                try: _icon = int(lines[1])
                except: _icon = 0
                try: _boardsize = int(lines[2])
                except: _boardsize = 4
                try: _maxboardsize = int(lines[3])
                except: _maxboardsize = 11
        except:
            _max = 1
            _icon = 0
            _boardsize = 4
            _maxboardsize = 11
        if _max > 100000:
            _max = 1
        if _icon not in range(0, 8):
            _icon = 0
        if _boardsize not in range(3, 34):
            _boardsize = 4
        if _maxboardsize < _boardsize or _maxboardsize not in range(3, 34):
            _maxboardsize = 11
        return [_max, _icon, _boardsize, _maxboardsize]

    def writeSettings(self, filename='data.bin'):
        var = self.getData()
        with open(filename, 'w') as file:
            file.write(str(var[0]) + '\n')
            file.write(str(var[1]) + '\n')
            file.write(str(var[2]) + '\n')
            file.write(str(var[3]) + '\n')
        
    def printBoard(self):
        clearConsole()
        print('2048 with Python ver', _version, ' (',str(self.__boardsize), 'x', str(self.__boardsize), ')')
        print('조작: WASD, 신규생성숫자: *, 설정: U, 게임 종료: Z')
        print('현재 점수: ', self.__curr, ', 현재 최고점수(숫자): ', end='')
        if self.__curr == self.__max:
            print('*', end='')
        print(self.__max)
        print()
        for x in range(self.__boardsize):
            for y in range(self.__boardsize):
                if x == self.__NUMBER.getX() and y == self.__NUMBER.getY():
                    print('*'+ str(self.getBoardData(x,y)), ' '*(self.__space-len(str(self.getBoardData(x,y)))), end='')
                elif self.getBoardData(x,y) == 0:
                    print(self.ICONS[self.__icon], ' '*(self.__space-len(str(self.getBoardData(x,y)))), end='')
                else: print(self.getBoardData(x,y), ' '*(self.__space-len(str(self.getBoardData(x,y)))+1), end='')
            for z in range(self.__space-1):
                print()
                
    def clearBoard(self):
        self.__isFinGame = False
        self.__curr = 1
        for x in range(self.__boardsize):
            for y in range(self.__boardsize):
                self.setBoardData(x,y,0)
                
    def updateScore(self):
        if self.__curr > self.__max:
            self.__max = self.__curr
            
    def FinishGame(self):
        self.__isFinGame = True
        self.__isOnGame = False
        
    def genNum(self):
        if self.hasNoSpace():
            self.__NUMBER.setPos(-1,-1)
            return
        while True:
            self.__NUMBER.genNumRandomly(self.__boardsize)
            if self.BOARD[self.__NUMBER.getX()][self.__NUMBER.getY()] == 0:
                self.BOARD[self.__NUMBER.getX()][self.__NUMBER.getY()] = self.__NUMBER.getValue()
                if self.BOARD[self.__NUMBER.getX()][self.__NUMBER.getY()] > self.__curr:
                    self.__curr = self.BOARD[self.__NUMBER.getX()][self.__NUMBER.getY()]
                    self.updateScore()
                return
            
    def checkDirAvailable(self, x, y, dir):
        if dir == 'Up':
            if x > 0: return True
            else: return False
        elif dir == 'Left':
            if y > 0: return True
            else: return False
        elif dir == 'Down':
            if x < self.__boardsize: return True
            else: return False
        elif dir == 'Right':
            if y < self.__boardsize: return True
            else: return False
        else: return False
        
    def isPlayAvailable(self):
        if self.__isFinGame:
            return False
        elif not self.hasNoSpace():
            return True
        for m in range(self.__boardsize-1, 0, -1):
                for n in range(0, self.__boardsize):
                        if self.BOARD[m-1][n] == 0:
                            self.BOARD[m-1][n] = self.BOARD[m][n]
                            self.BOARD[m][n] = 0
        for m in range(0, self.__boardsize-1):
            for n in range(0, self.__boardsize):
                if self.BOARD[m+1][n] == 0:
                    self.BOARD[m+1][n] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        for n in range(self.__boardsize-1, 0, -1):
            for m in range(0, self.__boardsize):
                if self.BOARD[m][n-1] == 0:
                    self.BOARD[m][n-1] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        for n in range(0, self.__boardsize-1):
            for m in range(0, self.__boardsize):
                if self.BOARD[m][n+1] == 0:
                    self.BOARD[m][n+1] = self.BOARD[m][n]
                    self.BOARD[m][n] = 0
        if self.hasNoSpace():
            for x in range(0, self.__boardsize):
                for y in range(0, self.__boardsize):
                    if self.BOARD[x][y] == self.BOARD[x+1][y] or self.BOARD[x][y] == self.BOARD[x][y+1] or self.BOARD[x][y] == self.BOARD[x-1][y] or self.BOARD[x][y] == self.BOARD[x][y-1]:
                        return True
            self.FinishGame()
            return False
        else: return True
        
    def hasNoSpace(self):
        for x in range(self.__boardsize):
            for y in range(self.__boardsize):
                if self.BOARD[x][y] == 0:
                    return False
        return True

    def applyDir(self, _dir):
        if _dir == 'Up':
            for x in range(1, self.__boardsize, 1):
                for y in range(0, self.__boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for m in range(self.__boardsize-1, 0, -1):
                            for n in range(0, self.__boardsize):
                                if self.getBoardData(m-1,n) == 0:
                                    self.setBoardData(m-1,n,self.getBoardData(m,n))
                                    self.setBoardData(m,n,0)
                    if self.getBoardData(x-1,y) == self.getBoardData(x,y):
                        self.setBoardData(x-1,y, self.getBoardData(x-1,y)*2)
                        self.setBoardData(x,y,0)
                        if self.getBoardData(x-1,y) > self.__curr:
                            self.__curr = self.getBoardData(x-1,y)
        elif _dir == 'Left':
            for y in range(1, self.__boardsize, 1):
                for x in range(0, self.__boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for n in range(self.__boardsize-1, 0, -1):
                            for m in range(0, self.__boardsize):
                                if self.BOARD[m][n-1] == 0:
                                    self.BOARD[m][n-1] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y-1] == self.BOARD[x][y]:
                        self.BOARD[x][y-1] *= 2
                        self.BOARD[x][y] = 0
                        if self.BOARD[x][y-1] > self.__curr:
                            self.__curr = self.BOARD[x][y-1]
        elif _dir == 'Down':
            for x in range(self.__boardsize-1, 0, -1):
                for y in range(0, self.__boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for m in range(0, self.__boardsize-1):
                            for n in range(0, self.__boardsize):
                                if self.BOARD[m+1][n] == 0:
                                    self.BOARD[m+1][n] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y] == self.BOARD[x-1][y]:
                        self.BOARD[x][y] *= 2
                        self.BOARD[x-1][y] = 0
                        if self.BOARD[x][y] > self.__curr:
                            self.__curr = self.BOARD[x][y]
        elif _dir == 'Right':
            for y in range(self.__boardsize-1, 0, -1):
                for x in range(0, self.__boardsize):
                    if self.checkDirAvailable(x, y, _dir):
                        for n in range(0, self.__boardsize-1):
                            for m in range(0, self.__boardsize):
                                if self.BOARD[m][n+1] == 0:
                                    self.BOARD[m][n+1] = self.BOARD[m][n]
                                    self.BOARD[m][n] = 0
                    if self.BOARD[x][y] == self.BOARD[x][y-1]:
                        self.BOARD[x][y] *= 2
                        self.BOARD[x][y-1] = 0
                        if self.BOARD[x][y] > self.__curr:
                            self.__curr = self.BOARD[x][y]
        self.updateScore()


def init():
    global _isExit
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
            MAIN.isOnGame(True)
            MAIN.clearBoard()
            break
        elif ans == 2:
            updateSettings()
        elif ans == 3:
            MAIN.FinishGame()
            _isExit = True
            return
        else: continue
    clearConsole()
    xPos = random.randint(0, MAIN.getData('boardsize')-1)
    yPos = random.randint(0, MAIN.getData('boardsize')-1)
    MAIN.setBoardData(xPos, yPos, 2)

def clearConsole():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')
    
def updateSettings():
    while True:
        clearConsole()
        MAIN.writeSettings(filename)
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
                print(MAIN.getData('icon')+1)
                inp = input('무엇으로 하시겠습니까? ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if inp not in range(1, len(MAIN.ICONS)+1):
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                MAIN.setData('null', inp-1, 'null')
                print('완료하였습니다. 계속하시려면 아무 키나 눌러주세요.')
                input() 
                break
        elif ans == 2:
            while True:
                print('판의 크기를 정해주세요.(정사각형, 추천: 4x4)')
                print('현재 판의 크기: ', end='')
                print(MAIN.getData('boardsize'))
                if not MAIN.isOnGame():
                    inp = input('숫자 하나를 입력해주세요(' + str(3) + '~' + str(MAIN.getData('maxboardsize')) + '): ')
                else:
                    inp = input('숫자 하나를 입력해주세요(' + str(MAIN.getData('boardsize')) + '~' + str(MAIN.getData('maxboardsize')) + '): ')
                try: inp = int(inp)
                except:
                    print('숫자가 아닙니다. 다시 입력해주세요.')
                    continue
                if MAIN.isOnGame() and inp < MAIN.getData('boardsize'):
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
                    continue
                elif inp in range(3, MAIN.getData('maxboardsize')+1):
                    MAIN.setData('null', 'null', inp)
                    print('완료하였습니다. 계속하시려면 아무 키나 눌러주세요.')
                    input()
                    break
                else:
                    print('범위를 초과하였습니다. 다시 입력해주세요.')
        elif ans == 3:
            break
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
    MAIN.writeSettings(filename)

def gameOver():
    global _isExit
    if not _isExit:
        MAIN.printBoard()
    while not _isExit:
        print('게임이 종료되었습니다. 다시하시겠습니까?')
        ans = input('다시시작: Y, 게임종료: N: ')
        if ans in ('Y', 'y', 'ㅇ'):
            MAIN.isOnGame(False)
            MAIN.isFinGame(False)
            return
        elif ans in ('N', 'n', 'ㄴ'):
            break
        else:
            print('잘못 입력하셨습니다. 다시 입력해주세요.')
            continue
        MAIN.clearBoard()
        MAIN.printBoard()
    print('게임을 종료하겠습니다. ', end='')
    if not _isExit:
        _isExit = True
        print('최고점수: ', MAIN.getData('max'))
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
        MAIN.isFinGame(True)
    elif key in ('U', 'u'):
        updateSettings()
    else:
        print('잘못 입력하셨습니다. 다시 입력해주세요.')
        getInput()

def _inGame():
    init()
    while not MAIN.isFinGame():
        MAIN.genNum()
        if not MAIN.isPlayAvailable():
            break
        MAIN.printBoard()
        getInput()
        print()

def inGame():
    while not _isExit:
        _inGame()
        MAIN.writeSettings(filename)
        gameOver()

filename = 'data.bin'
MAIN = G2048(filename)
inGame()
