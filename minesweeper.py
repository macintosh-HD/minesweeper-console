from IPython.display import clear_output
import os
import time
import readchar
import typing
import random as rand

class Board:
    # width: int
    # height: int
    # mines: int
    #
    # fields = []
    # played = False
    #
    # playerX = 0
    # playerY = 0

    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines
        self.played = False

        self.playerX = 0
        self.playerY = 0

        self.fields = []
        for h in range(height):
            for w in range(width):
                self.fields.append(Field(w,h,False))

    def generateMines(self):
        for mine in range(self.mines):
            placed = False
            while not placed:
                x = round(rand.uniform(0,self.width))
                y = round(rand.uniform(1,self.height + 1))
                if not self.fields[x*y].mine and not self.fields[x*y].discovered:
                    self.fields[x*y].placeMine()
                    placed = True

    def getMinesLeft(self):
        mineCounter = 0
        for field in self.fields:
            if field.isMineUnderneath():
                mineCounter += 1
        return mineCounter

    # def printBoard(self, gameTime):
    def printBoard(self):
        clear_output()
        os.system('clear')

        aChar = 97
        currChar = aChar

        print("Mines: " + str(self.getMinesLeft())) # + "    " + "Time: %.0fs" % gameTime)
        print()

        # print first line of board
        line = "  "
        for w in range(self.width):
            line += chr(currChar) + "  "
            currChar += 1
        print(line)

        # print actual board
        currChar = aChar
        for h in range(self.height):
            # append line character
            line = chr(currChar)
            currChar += 1
            for w in range(self.width):
                if self.playerAtPosition(w,h):
                    line += "["
                else:
                    line += " "

                currField = self.fields[w*(h + 1)]

                if currField.isFlagged():
                    line += "f"
                elif currField.isDiscovered():
                    line += "_"
                else:
                    line += "#"

                if self.playerAtPosition(w,h):
                    line += "]"
                else:
                    line += " "
            print(line)

    def playerAtPosition(self,x,y):
        if self.playerX == x and self.playerY == y:
            return True
        else:
            return False

    def movePlayerUP(self):
        self.playerY = (self.playerY - 1) % self.height

    def movePlayerLEFT(self):
        self.playerX = (self.playerX - 1) % self.width

    def movePlayerDOWN(self):
        self.playerY = (self.playerY + 1) % self.height

    def movePlayerRIGHT(self):
        self.playerX = (self.playerX + 1) % self.width

    def toggleFlag(self):
        field = self.fields[self.playerX * (1 + self.playerY)]
        field.flagged = field.flagged and True

    def discoverField(self):
        field = self.fields[self.playerX * (1 + self.playerY)]
        if field.isMineUnderneath():
            return False
        if not self.played:
            self.played = True
            self.generateMines()
        self.openFields(self.playerX, self.playerY)
        return True

    def openFields(self, x: int, y: int):
        field = self.fields[x * (y + 1)]
        if not field.isDiscovered():
            field = field.discover()
            if field.minesInSurrounding == 0:
                if x > 0:
                    self.openFields(x - 1, y)
                if x < self.width:
                    self.openFields(x + 1, y)
                if y > 0:
                    self.openFields(x, y - 1)
                if y < self.height:
                    self.openFields(x, y + 1)

    def isFinished(self):
        finished = True
        for h in range(self.height):
            for w in range(self.width):
                field = self.fields[w * (h + 1)]
                if field.isMineUnderneath() and field.isFlagged():
                    finished = finished and True
                elif field.isMineUnderneath() and not field.isFlagged():
                    finished = finished and False

class Field:
    # x: int
    # y: int
    # mine: bool
    # flagged: bool
    # minesInSurrounding: int
    # discovered: bool

    def __init__(self, x: int, y: int, mine: bool):
        self.x = x
        self.y = y
        self.mine = mine
        self.flagged = False
        self.minesInSurrounding = 0
        self.discovered = False

    def toggleFlag(self):
        self.flagged = not self.flagged

    def isFlagged(self):
        return self.flagged

    def placeMine(self):
        self.mine = True

    def setNeighbourMines(self, mines: int):
        self.minesInSurrounding = mines

    def getNeighbourMines(self):
        return self.minesInSurrounding

    def isMineUnderneath(self):
        return self.mine

    def isDiscovered(self):
        return self.discovered

    def discover(self):
        self.discovered = True

class Minesweeper:
    board = None
    startTime = 0

    def __init__(self):
        self.gameLoop()

    def gameLoop(self):
        while True:
            keyboard_input = readchar.readchar()
            print(keyboard_input)
            if not self.inputHandler(keyboard_input):
                break
            if self.board is not None:
                # self.board.printBoard(self.gameTime())
                self.board.printBoard()
                if self.board.isFinished():
                    print("You won!")
                    return
        print("You lost!")
        self.inputHandler('q')

    def inputHandler(self, keyboard_input):
        if keyboard_input == 'q':
            quit()
        elif keyboard_input == 'w':
            self.board.movePlayerUP()
        elif keyboard_input == 'a':
            self.board.movePlayerLEFT()
        elif keyboard_input == 's':
            self.board.movePlayerDOWN()
        elif keyboard_input == 'd':
            self.board.movePlayerRIGHT()
        elif keyboard_input == 'f':
            self.board.toggleFlag()
        elif keyboard_input == 'g':
            return self.board.discoverField()
        elif keyboard_input == 'n':
            self.new_game()
        else:
            print("Invalid input!")
            time.sleep(1)
        return True

    def new_game(self):
        clear_output()
        os.system('clear')
        print("NEW GAME STARTED")
        time.sleep(1)
        clear_output()
        os.system('clear')

        self.board = Board(8, 8, 5)
        self.startTime = time.time()

    # def gameTime(self):
    #     return time.time() - self.startTime

Minesweeper()
