import pygame as pg
import random  

pg.init()

length = 700

cubeLength = 25

white = (255, 255, 255)
black = (0, 0, 0)
foodColor = (0, 255, 204)

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

    def getList(self):
        return self.listCubes
    
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
        # makes sure it doesn't move out of screen, but if it does moves to other side of screen
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
        elif self.listCubes[0].getX() >= length:
            self.listCubes[0].setX(self.listCubes[0].getX() - length)
            self.draw()
        elif self.listCubes[0].getX() < 0:
            self.listCubes[0].setX(self.listCubes[0].getX() + length)
            self.draw()
            
        # y correction 
        elif self.listCubes[0].getY() >= length:
            self.listCubes[0].setY(self.listCubes[0].getY() - length)
            self.draw()
        elif self.listCubes[0].getY() < 0:
            self.listCubes[0].setY(self.listCubes[0].getY() + length)
            self.draw()



class Food():
    def __init__(self, snake):
        self.newFood(snake)
        self.length = cubeLength
            
    def newFood(self, snake):
        '''Spawns a new food on a random position on the screen and then 
        checks if that position is in the snake, and if so it calls itself and creates a new location'''
        snake = Snake.getList(snake)
        self.x = random.randint(0, (length - cubeLength) / cubeLength) * cubeLength
        self.y = random.randint(0, (length - cubeLength) / cubeLength) * cubeLength
        
        
        for cube in snake:
            if self.x == cube.getX() and self.y == cube.getY():
                self.x = random.randint(0, (length - cubeLength) / cubeLength) * cubeLength
                self.y = random.randint(0, (length - cubeLength) / cubeLength) * cubeLength
        
        if self.x == cube.getX() and self.y == cube.getY():
            self.newFood(snake)
    
    def ifEaten(self, Snake):
        if (
            Snake.getList()[0].getX() == self.x and 
            Snake.getList()[0].getY() == self.y 
            ): 
            Snake.addCube()
            self.newFood(Snake)
    
    def draw(self):
        pg.draw.rect(surface, foodColor, ((self.x, self.y), (self.length, self.length)))


def checkCollisions(Snake):
    for cube in Snake.getList():
        if (
            cube.getX() == Snake.getList()[0].getX() and # checks if head shares same x coordinate
            cube.getY() == Snake.getList()[0].getY() and # chekcs if head shares same y coordinate
            Snake.getList().index(cube) != 1 and  # prevents unintended "collision" of first body piece hitting head
            Snake.getList().index(cube) != 0 # prevents checking if the head position equals the head position
            ):
                collision()

def collision():
    print("collision")
    pg.quit()
    quit()
    # could make this go to a loss screen 


def main():
    loop = True
    # clock = pg.time.Clock()

    # initializes snake and starts it off with some length
    snake = Snake()
    snake.addCube()
    snake.addCube()


    snake.draw()

    direction = "right"
    
    food = Food(snake)
    
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
                        break # prevents bug of rapidly turning up and right resulting in turning into yourself
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    if direction != "down":
                        direction = "up"
                        break # prevents bug of rapidly turning up and right resulting in turning into yourself
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    if direction != "up":
                        direction = "down"
                        break # prevents bug of rapidly turning up and right resulting in turning into yourself
                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    if direction != "right":
                        direction = "left"
                        break # prevents bug of rapidly turning up and right resulting in turning into yourself


        eraseScreen()
        food.ifEaten(snake)
        food.draw()
        # move body first to get the position of head (for the body piece behind head) before head is moved
        snake.moveBody() 
        snake.moveHead(direction)


        pg.display.update()
        checkCollisions(snake)

if __name__ == "__main__":
    main()

pg.quit()
quit()

# TODO fix bugs, work on interface / colors, make it so when the body of the snake hits food it gets eaten so food doesn't spawn within the snake (or make it so it can't spawn within the snake)
# ! BUG: when eating food and going to edge of screen snake dies
    # after the snake eats food if its body is going to the end of the screen it dies 

# could have it where every food is a random color and then the snake takes on this random color when it eats it or the cube thats added is the food color 
# could add smile and eyes to snake head
# sound when snake is eaten 
# high score 
# loss screen 
