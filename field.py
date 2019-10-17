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

