import turtle
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title("COVID BATTLE BY WAYSTER  DE MELO")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.level = 1

    def start_level(self):
        sprites.clear()

        sprites.append(player)
        sprites.append(missile)

        #add enemies
        for _ in range(self.level):
            x = random.randint(-self.width/2, self.width/2)
            y = random.randint(-self.height/2, self.height/2)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, -2)
            sprites.append(Enemy(x,y,"square","red"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy

            #add powerups
        for _ in range(self.level):
            x = random.randint(-self.width/2, self.width/2)
            y = random.randint(-self.height/2, self.height/2)
            dx = random.randint(-2, 2)
            dy = random.randint(-2, -2)
            sprites.append(Powerup(x,y,"circle","blue"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy

    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()
        
        left = -self.width/2.0 - x_offset
        right = self.width/2.0 - x_offset
        top = self.height/2.0 - y_offset
        bottom = -self.height/2.0 - y_offset

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()

class Sprite():
    #constructor
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx= 0
        self.dy = 0    
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.1
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"


    def is_collision(self, other):
        if self.x < other.x + other.width and\
            self.x + self.width > other.x and\
            self.y < other.y + other.height and\
            self.y + self.height > other.y:
            return True  
        else:
         return False

    def bounce(self, other):
        temp_dx = self.dx
        temp_dy = self.dy
        self.dx = other.dx
        self.dy = other.dy
        other.dx = temp_dx
        other.dy = temp_dy 
   
    def update(self):

        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

        self.x += self.dx
        self.y += self.dy

        self.border_check()

    def border_check(self):
        if self.x > game.width/2.0 - 10:
            self.x = game.width/2.0 - 10
            self.dx *= -1
        elif self.x < -game.width/2.0 + 10:
            self.x = -game.width/2.0 + 10
            self.dx *= -1    

        if self.y > game.height/2.0 - 10:
            self.y = game.height/2.0 - 10
            self.dy *= -1

        elif self.y < -game.height/2.0 + 10:
            self.y = -game.height/2.0 + 10
            self.dy *= -1     

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.goto(self.x - x_offset,  self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            self.render_health_meter(pen, x_offset, y_offset)

    #draw health meter
    def render_health_meter(self, pen, x_offset, y_offset):
        pen.goto(self.x - x_offset - 10, self.y - y_offset + 20)
        pen.width(3)
        pen.pendown()
        pen.setheading(0)

        if self.health/self.max_health < 0.3:
            pen.color("red")
        elif self.health/self.max_health < 0.7:
            pen.color("yellow")
        else:
            pen.color("green")

        pen.fd(20 * (self.health/self.max_health)) 
        pen.color( "grey")
        pen.fd(20 * ((self.max_health-self.health)/self.max_health)) 

        pen.penup()   

class Player(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0
    
    def rotate_left(self):
        self.da = 5

    def rotate_right(self):
        self.da = -5

    def stop_rotating(self):
        self.da = 0

    def accelerate(self):
        self.thrust += self.acceleration

    def desaccelaration(self):
        self.thrust = 0.0 

    def fire(self):
        missile.fire(self.x, self.y, self.heading, self.dx, self.dy)

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360
            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust
            self.x += self.dx
            self.y += self.dy
            self.border_check()
            #check health 
            if self.health <= 0:
                self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.health = self.max_health
        self.heading = 90
        self.dx = 0
        self.dy = 0
        self.lives -= 1


    def render(self, pen, x_offset, y_offset):
        pen.shapesize(0.5, 1.0, None)
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        pen.shapesize(1.0, 1.0, None)
        self.render_health_meter(pen, x_offset, y_offset)

class Missile(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        self.state = "ready"
        self.max_fuel = 300
        self.fuel = self.max_fuel
        self.thrust = 8.0
        self.height = 4
        self.width = 4

    def fire(self, x, y, heading, dx, dy):
        self.state = "active"
        self.x = x
        self.y = y
        self.heading = heading
        self.dx = dx
        self.dy = dy

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360
            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust
            self.x += self.dx
            self.y += self.dy
            self.border_check()
            #check health 
            if self.health <= 0:
                self.reset()

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(0.2, 0.2, None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(1.0, 1.0, None)


    def update(self):
        if self.state == "active":  
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.reset() 

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.fuel = self.max_fuel
        self.dx = 0
        self.dy = 0
        self.state = "ready"

class Enemy(Sprite): 
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        self.max_health = 20
        self.health = self.max_health
    
    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360
            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust
            self.x += self.dx
            self.y += self.dy
            self.border_check()
            #check health 
            if self.health <= 0:
                self.reset()

    def reset(self):
        self.state = "inactive"    

class Powerup(Sprite): 
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)

class Camera():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y


#create missile obj
missile = Missile(0, 100, "circle", "yellow")

#create game obj
game = Game(800, 600)

#create player
player = Player(0, 0, "triangle", "white")

#create camera obj
camera = Camera(player.x, player.y)

#sprites list 
sprites = []
#setup the level
game.start_level()

#keyboard binding
wn.listen()
wn.onkeypress(player.rotate_left, "Left")
wn.onkeypress(player.rotate_right, "Right")
 
wn.onkeyrelease(player.stop_rotating, "Left")
wn.onkeyrelease(player.stop_rotating, "Right")

wn.onkeypress(player.accelerate, "Up")
wn.onkeyrelease(player.desaccelaration, "Up")

wn.onkeypress(player.fire, "space")

#mainloop
while True:
    #clear screen
    pen.clear()

    #do game stuff

    #update sprites 
    for sprite in sprites:
        sprite.update()

    #check for collision 
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            if player.is_collision(sprite):
               sprite.health -= 10
               player.health -= 10
               player.bounce(sprite)
        
            if missile.state == "active" and missile.is_collision(sprite):
                sprite.health -= 10
                missile.reset()

        if isinstance(sprite, Powerup):
            if player.is_collision(sprite):
                sprite.x = 100
                sprite.y = 100  

            if missile.state == "active" and missile.is_collision(sprite):
                sprite.x = 100
                sprite.y = -100   
                missile.reset()       


    #render sprites
    for sprite in sprites:
        sprite.render(pen, camera.x, camera.y)
   
    game.render_border(pen, camera.x, camera.y)

    #check for end of level/
    end_of_level = True
    for sprite in sprites:
        #look for an active enemy
        if isinstance(sprite, Enemy) and sprite.state == "active":
            end_of_level = False
    if end_of_level:
        game.level += 1
        game.start_level()

    #update camera 
    camera.update(player.x, player.y)

    #update the screen
    wn.update()