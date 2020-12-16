import random
import re

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
        elif self.getNearBombs(posX,posY) > 0:
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

    def __str__(self):
        string = '   '
        for i in range(self.width):
            string += str(i) + ' '
        for x in range(self.width):
            string += '\n'+ str(x) +' |'
            for y in range(self.height):
                if (x,y) in self.points:
                    if self.getNearBombs(x,y) == 0:
                        string += ' |'
                    else:
                        string += str(self.getNearBombs(x,y)) + '|'
                else:
                    string += '#'+'|'
        return string

    def printB(self):
        string = '   '
        for i in range(self.width):
            string += str(i) + ' '
        for x in range(self.width):
            string += '\n'+ str(x) +' |'
            for y in range(self.height):
                if self.board[x][y] == 9:
                    string += 'X|'
                else:
                    string += ' |'
        print(string)

def Start():
    #Board(w,h,c) -> Board of w*h with bomb count 'c'
    b = Board(10,10,20)
    b.printB()
    while True:
        print(b)
        position = re.split(',(\\s)*',input("Select any position(x,y): "))
        x,y = int(position[0]),int(position[-1])
        if (x < 0 or x >= b.width) and (y > 0 or y >= b.height):
            print("Invalid Position")
            continue
        if b.isSafe(x,y):
            b.select(x,y)
        else:
            print("\n-----You Lose-----")
            b.printB()
            break
        if len(b.points) == b.height * b.height - b.bombCount:
            print("\n-----You Win-----")
            break

if __name__ == "__main__":
    Start()