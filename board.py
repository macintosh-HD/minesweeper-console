from IPython.display import clear_output
import random as rand
import os

import field as f

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
                self.fields.append(f.Field(w,h,False))

    def generateMines(self):
        for mine in range(self.mines):
            placed = False
            while not placed:
                x = round(rand.uniform(0,self.width))
                y = round(rand.uniform(1,self.height + 1))
                if not self.fields[x*y].mine and not self.fields[x*y].discovered:
                    self.fields[x*y].placeMine()
                    placed = True
        self.initializeFields()

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
                # print(currField)

                if currField.isFlagged():
                    line += "f"
                elif currField.isDiscovered() and currField.minesInSurrounding == 0:
                    line += "_"
                elif currField.isDiscovered():
                    line += str(currField.minesInSurrounding)
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
            field.discover()
            self.generateMines()
            field.discovered = False
        self.openFields(self.playerX, self.playerY)
        return True

    def openFields(self, x: int, y: int):
        field = self.fields[x * (y + 1)]
        if not field.isDiscovered() and not field.isMineUnderneath():
            # field = field.discover()
            field.discover()
            if field.minesInSurrounding == 0:
                if x > 0:
                    self.openFields(x - 1, y)
                if x < self.width - 1:
                    self.openFields(x + 1, y)
                if y > 0:
                    self.openFields(x, y - 1)
                if y < self.height - 1:
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

    def initializeFields(self):
        for h in range(self.height):
            for w in range(self.width):
                fieldIndex = w * (h + 1)
                minesInSurrounding = self.getMinesInSurroundingForField(w, h)
                print(minesInSurrounding)
                self.fields[fieldIndex].setNeighbourMines(minesInSurrounding)

    def getMinesInSurroundingForField(self, x: int, y: int):
        minesInSurrounding = 0
        for newX in range(x - 1, x + 2):
            for newY in range(y - 1, y + 2):
                if x >= 0 and x < self.width and y >= 0 and y < self.height and not x == newX and not y == newY and self.fields[x * (y + 1)].isMineUnderneath():
                    minesInSurrounding += 1
        return minesInSurrounding