import random

class Vehicle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.source = []
        self.destination = []

    def moveRight(self,x,y,screen):
        if screen[x][y+1] == " ":
            screen[x][y] = " "
            screen[x][y+1] = 'O'
            self.x, self.y = x ,y+1
            return True
        return False

    def moveLeft(self,x,y,screen):
        if screen[x][y-1] == " ":
            screen[x][y] = " "
            screen[x][y-1] = 'O'
            self.x, self.y = x ,y-1
            return True
        return False

    def moveUp(self,x,y,screen):
        if screen[x-1][y] == " ":
            screen[x][y] = " "
            screen[x-1][y] = 'O'
            self.x, self.y = x-1 ,y
            return True
        return False

    def moveDown(self,x,y,screen):
        if screen[x+1][y] == " ":
            screen[x][y] = " "
            screen[x+1][y] = 'O'
            self.x, self.y = x+1 ,y
            return True
        return False

    def isAccomodate(self,x,y,screen):
        if(screen[x][y] == ' '):
            return True
        return False

    def motion(self,screen):
        count = 0
        while count < 10:
            direction = random.randint(1,5)
            if direction==1:
                if self.moveUp(self.x, self.y, screen):
                    break

            elif direction==2:
                if self.moveDown(self.x, self.y,screen):
                    break

            elif direction==3:
                if self.moveRight(self.x, self.y,screen):
                    break

            elif direction==4:
                if self.moveLeft(self.x, self.y,screen):
                    break
            count+=1
