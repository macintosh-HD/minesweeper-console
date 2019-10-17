from IPython.display import clear_output
import os
import time
import readchar
import typing
import random as rand

import board as b

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

        self.board = b.Board(8, 8, 5)
        self.startTime = time.time()

    # def gameTime(self):
    #     return time.time() - self.startTime

Minesweeper()
