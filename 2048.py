import random
import os

_MAPSIZE = 4
_SPACE = 4
_isFinished = False
map = [[0 for col in range(4)] for row in range(4)]

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def printMap():
    clearConsole()
    for x in range(_MAPSIZE):
        for y in range(_MAPSIZE):
            print(map[x][y], ' '*(_SPACE-len(str(map[x][y]))+1), end='')
        for z in range(_SPACE):
            print()

def makeitRandom():
    for x in range(_MAPSIZE*100):
        xpos = random.randint(0,_MAPSIZE-1)
        ypos = random.randint(0,_MAPSIZE-1)
        if map[xpos][ypos] == 0:
            map[xpos][ypos] = 2
            return
    
    
        
def checkIsFinished():
    global _isFinished
    hasZero = False
    for x in range(_MAPSIZE):
        for y in range(_MAPSIZE):
            if map[x][y] == 2048:
                _isFinished = True
                return True
    
    return False
def getInput():
    key = input('방향: ')
    if key == 'w':
        applyDir('UP')
    elif key == 'a':
        applyDir('LEFT')
    elif key == 's':
        applyDir('DOWN')
    elif key == 'd':
        applyDir('RIGHT')
    else:
        print('잘못 입력하셨습니다. 다시 시도해주세요.')
        getInput()
        
def checkAvailableDir(x, y, dir):
    if dir == 'UP':
        if x>0: return True
        else: return False
    if dir == 'DOWN':
        if x<_MAPSIZE: return True
        else: return False
    if dir == 'LEFT':
        if y>0: return True
        else: return False
    if dir == 'RIGHT':
        if y<_MAPSIZE: return True
        else: return False
    
            
def applyDir(_dir):
    if _dir == 'UP':
        for x in range(1, _MAPSIZE, 1):
            for y in range(0, _MAPSIZE):
                if checkAvailableDir(x,y,_dir) == True:
                        for m in range(_MAPSIZE-1, 0, -1):
                            for n in range(0, _MAPSIZE):
                                if map[m-1][n] == 0:
                                    map[m-1][n] = map[m][n]
                                    map[m][n] = 0
                if map[x-1][y] == map[x][y]:
                    map[x-1][y]*=2
                    map[x][y]=0

    elif _dir == 'DOWN':
        for x in range(_MAPSIZE-1, 1, -1):
            for y in range(0, _MAPSIZE):
                if checkAvailableDir(x,y,_dir) == True:
                        for m in range(0, _MAPSIZE-1, 1):
                            for n in range(0, _MAPSIZE):
                                if map[m+1][n] == 0:
                                    map[m+1][n] = map[m][n]
                                    map[m][n] = 0
                if map[x-1][y] == map[x][y]:
                    map[x][y]*=2
                    map[x-1][y]=0
    elif _dir == 'LEFT':
        for y in range(1, _MAPSIZE, 1):
            for x in range(0, _MAPSIZE):
                if checkAvailableDir(x,y,_dir) == True:
                        for n in range(_MAPSIZE-1, 0, -1):
                            for m in range(0, _MAPSIZE):
                                if map[m][n-1] == 0:
                                    map[m][n-1] = map[m][n]
                                    map[m][n] = 0
                if map[x][y] == map[x][y-1]:
                    map[x][y-1]*=2
                    map[x][y]=0

    elif _dir == 'RIGHT':
        for y in range(_MAPSIZE-1, 1, -1):
            for x in range(0, _MAPSIZE):
                if checkAvailableDir(x,y,_dir) == True:
                        for n in range(0, _MAPSIZE-1, 1):
                            for m in range(0, _MAPSIZE):
                                if map[m][n+1] == 0:
                                    map[m][n+1] = map[m][n]
                                    map[m][n] = 0
                if map[x][y-1] == map[x][y]:
                    map[x][y]*=2
                    map[x][y-1]=0
                    
            
print('조작: WASD')
while _isFinished == False:
    makeitRandom()
    printMap()
    getInput()
