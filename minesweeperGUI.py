from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import sys,random,re

class Board():
    def __init__(self,width,height,bombCount):
        self.width = width
        self.height = height
        self.bombCount = bombCount
        self.board = self.createBoard()
        self.points = set()

    def createBoard(self):
        board = [[0 for x in range(self.width)] for y in range(self.height)]
        count = 0
        while count < self.bombCount:
            x = random.randint(0,self.width-1)
            y = random.randint(0,self.height-1)
            board[x][y] = 9
            count += 1
        return board

    def isSafe(self,x,y):
        if self.board[x][y] == 9:
            return False
        else:
            return True

    def select(self,posX,posY):
        self.points.add((posX,posY))
        if self.board[posX][posY] == 9:
            return False
        if self.getNearBombs(posX,posY) > 0:
            return True
        for x in range(max(0,posX-1),min(self.width-1,posX+1)+1):
            for y in range(max(0,posY-1),min(self.height-1,posY+1)+1):
                if (x,y) in self.points:
                        continue
                self.select(x,y)
        return True    

    def getNearBombs(self,posX,posY):
        count = 0
        for x in range(max(0,posX-1),min(self.width-1,posX+1)+1):
            for y in range(max(0,posY-1),min(self.height-1,posY+1)+1):
                if x == posX and y == posY:
                    continue
                if self.board[x][y] == 9:
                    count += 1
        return count

class Button(QPushButton):
    def __init__(self, posX, posY, size, parent):
        super(Button, self).__init__(parent)
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.init(posX,posY,size)

    def init(self, x, y, s):
        self.setGeometry(10+x*s,10+y*s, s, s)

    def buttonClicked(self):
        self.parent.click(self.posY,self.posX)

class Window(QMainWindow):
    def __init__(self,width,height,bombCount):
        super(Window,self).__init__()
        self.width = width
        self.height = height
        self.bombCount = bombCount
        self.buttons = [[Button(x,y,40,self) for x in range(self.width)] for y in range(self.height)]
        self.board = Board(self.width,self.height,self.bombCount)
        self.setupButtons()

    def setupButtons(self):
        for x in range(self.width):
            for y in range(self.height):
                self.buttons[x][y].clicked.connect(self.buttons[x][y].buttonClicked)

    def click(self,posX,posY):
        if self.board.isSafe(posX,posY):
            self.board.select(posX,posY)
            for x in range(self.width):
                for y in range(self.height):
                    if (x,y) in self.board.points:
                        if self.board.getNearBombs(x,y) > 0:
                            self.buttons[x][y].setText(str(self.board.getNearBombs(x,y)))
                        self.buttons[x][y].setEnabled(False)
        else:
            for x in range(self.width):
                for y in range(self.height):
                    if self.board.board[x][y] == 9:
                        self.buttons[x][y].setText("X")
                    elif self.board.getNearBombs(x,y) > 0:
                        self.buttons[x][y].setText(str(self.board.getNearBombs(x,y)))
            self.showPopup("You Lose","You clicked on a bomb")

        if len(self.board.points) == (self.width*self.height) - self.bombCount:
            for x in range(self.width):
                for y in range(self.height):
                    if self.board.board[x][y] == 9:
                        self.buttons[x][y].setText("X")
                    elif self.board.getNearBombs(x,y) > 0:
                        self.buttons[x][y].setText(str(self.board.getNearBombs(x,y)))
            self.showPopup("You Win!","Congratulation you win")

    def showPopup(self,title,text):
        popup = QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(text)
        x = popup.exec_()

def Start(width, height, bombCount):
    app = QApplication(sys.argv)
    win = Window(width,height,bombCount)
    win.setGeometry(0,0,(width*40)+20,(height*40)+20)
    win.setWindowTitle("Minesweeper")
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    #Board of szie 10x10 containing 15 bombs
    Start(10,10,15)