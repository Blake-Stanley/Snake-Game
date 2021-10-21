import pygame as pg
import math 

pg.init()

length = 700

cubeLength = 25

white = (255, 255, 255)
black = (0, 0, 0)

surface = pg.display.set_mode((length, length))
pg.display.set_caption("Snake Game")

screen = pg.display.set_mode((length, length))


def eraseScreen():
    pg.draw.rect(surface, black, ((0, 0), (length, length)))


class Cube:
    """
    parameters x and y are coordinates on screen
    cubes have direction to allow for movement logic
    """

    def __init__(self, x, y, direction):
        self.length = cubeLength
        self.x = x
        self.y = y
        self.direction = direction

    def draw(self):
        pg.draw.rect(surface, white, ((self.x, self.y), (self.length, self.length)))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getDir(self):
        return self.direction

    def move(self, direction):
        if direction == "right":
            self.x += cubeLength
        elif direction == "left":
            self.x -= cubeLength
        elif direction == "down":
            self.y += cubeLength
        elif direction == "up":
            self.y -= cubeLength

    def set_dir(self, direction):
        self.direction = direction


class Snake:
    def __init__(self):
        self.listCubes = [Cube(length / 2, length / 2, "right")]

    # todo test if this works
    # adds a cube to the end of the snake, to the left if its going right, down if its going up, etc.
    def addCube(self):
        direction = self.listCubes[len(self.listCubes) - 1].getDir()

        if direction == "right":
            offsetX = cubeLength
            offsetY = 0

        elif direction == "left":
            offsetX = -1 * cubeLength
            offsetY = 0

        elif direction == "up":
            offsetX = 0
            offsetY = -1 * cubeLength

        elif direction == "down":
            offsetX = 0
            offsetY = cubeLength

        x = self.listCubes[len(self.listCubes) - 1].getX() - offsetX
        y = self.listCubes[len(self.listCubes) - 1].getY() - offsetY

        self.listCubes.append(Cube(x, y, direction))

    # draw the snake by drawing all the individual cubes
    def draw(self):
        for cube in self.listCubes:
            cube.draw()

    # checks cube in front of it and takes its position (done this way so that the snake can turn)
    def moveBody(self):
        for i in range(len(self.listCubes) - 1, 0, -1):
            self.listCubes[i].setX(self.listCubes[i - 1].getX())
            self.listCubes[i].setY(self.listCubes[i - 1].getY())
            self.listCubes[i].draw()

    # moves head up, down, left, or right 1 square
    def moveHead(self, direction):
        # make sure it doesn't move out of screen, but if it does moves to other side of screen
        if (# x boundary  
            self.listCubes[0].getX() >= 0
            and self.listCubes[0].getX() <= length - cubeLength
            # y boundary 
            and self.listCubes[0].getY() >= 0
            and self.listCubes[0].getY() <= length - cubeLength
        ):
            self.listCubes[0].move(direction)
            self.draw()
            
        # x correction 
        elif self.listCubes[0].getX() >= length - cubeLength:
            self.listCubes[0].setX(self.listCubes[0].getX() - length)
            self.draw()
        elif self.listCubes[0].getX() <= 0:
            self.listCubes[0].setX(self.listCubes[0].getX() + length)
            self.draw()
            
        # y correction 
        elif self.listCubes[0].getY() >= length - cubeLength:
            self.listCubes[0].setY(self.listCubes[0].getY() - length)
            self.draw()
        elif self.listCubes[0].getY() <= 0:
            self.listCubes[0].setY(self.listCubes[0].getY() + length)
            self.draw()

    # def move(self, direction):
    #     self.moveBody()
    #     self.moveHead(direction)


class Food(Cube):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        

def newFood():
    x = math.randomInt(0, length - cubeLength)
    y = math.randomInt(0, length - cubeLength)
    food = Food()
    food.draw()

# TODO make a function that draws the food randomly, check if head collides, addCube() if it does


def main():
    loop = True
    # clock = pg.time.Clock()

    # initializes snake and starts it off with some length
    snake = Snake()
    snake.addCube()
    snake.addCube()
    snake.addCube()
    snake.addCube()
    snake.addCube()

    snake.draw()

    direction = "right"
    while loop:
        pg.time.delay(80)
        # clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d or event.key == pg.K_RIGHT:
                    if direction != "left":
                        direction = "right"
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    if direction != "down":
                        direction = "up"
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    if direction != "up":
                        direction = "down"
                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    if direction != "right":
                        direction = "left"

        eraseScreen()
        # move body first to get the position of head (for the body piece behind head) before head is moved
        snake.moveBody() 
        snake.moveHead(direction)
        pg.display.update()


if __name__ == "__main__":
    main()

pg.quit()
quit()

# TODO collision detection 
