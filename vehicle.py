import random

class Vehicle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.source = []
        self.destination = []
        self.present_road = ""
        self.present_junction = ""

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
        if(screen[x][y] != 'X'):
            return True
        return False

    def random_motion(self,screen):
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

    def traverseToJunction(self, junctions, junction, city_map):
        x_pos, y_pos = self.x, self.y
        junc_x, junc_y = junctions[junction][0], junctions[junction][1]

        if x_pos == junc_x:
            if y_pos < junc_y:
                self.moveRight(x_pos, y_pos,city_map)
            else:
                self.moveLeft(x_pos, y_pos,city_map)

        if y_pos == junc_y:
            if x_pos < junc_x:
                self.moveDown(x_pos, y_pos,city_map)
            else:
                self.moveUp(x_pos, y_pos,city_map)

        if x_pos-1 == junc_x:
            if y_pos < junc_y:
                self.moveRight(x_pos, y_pos,city_map)
            else:
                self.moveLeft(x_pos, y_pos,city_map)

        if y_pos-1 == junc_y:
            if x_pos < junc_x:
                self.moveDown(x_pos, y_pos,city_map)
            else:
                self.moveUp(x_pos, y_pos,city_map)
