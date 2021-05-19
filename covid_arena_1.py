import turtle

SCREEN_WIDTH = 800;
SCREEN_HEIGHT = 600;

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

class Sprite():
    #constructor
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

#create player
player = Sprite(0,0,"triangle","white")
enemy = Sprite(0,100,"square","red")
powerup = Sprite(0, -100, "circle", "blue")



#mainloop
while True:
    #clear screen
    pen.clear()

    #do game stuff
    #render sprites
    player.render(pen)
    enemy.render(pen)
    powerup.render(pen)

    #update the screen
    wn.update()