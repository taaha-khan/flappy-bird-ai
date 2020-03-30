import turtle
import random
import time

width = 475
height = 650

pipePairDistance = 100
pipeDistance = 150
pipeHeight = 400
pipeWidth = 80
pipeSpeed = 3

wn = turtle.Screen()
wn.title('Flappy Bird')
wn.setup(width, height)
wn.bgcolor('light blue')
wn.bgpic('flappybg.gif')
wn.tracer(0)

wn.register_shape('pipe', ((-pipeWidth/2, pipeHeight/2), (pipeWidth/2, pipeHeight/2), (pipeWidth/2, -pipeHeight/2), (-pipeWidth/2, -pipeHeight/2)))
wn.register_shape('bird.gif')
wn.register_shape('pipe.gif')
wn.register_shape('pipe2.gif')

floor = turtle.Turtle()
floor.speed(0)
floor.color('black')
floor.width(4)
floor.pu()
floor.ht()

ground = -250

floor.goto(-width/2, ground)
floor.pd()
floor.goto(width/2, ground)

bird = turtle.Turtle()
bird.shape('bird.gif')
bird.speed(0)
bird.pu()
bird.setpos(-50, 0)
bird.score = 0

scorer = turtle.Turtle()
scorer.speed(0)
scorer.ht(); scorer.pu()
scorer.color('black')
scorer.goto(0, height/2 - 120)

def updateScore():
    scorer.clear()
    scorer.write(bird.score, move=False, align="center", font=("Courier", 30, "bold"))


bird.dy = 0
gravity = -0.4

def jump():
    bird.dy += 13

def click(x, y):
    bird.dy += 13


wn.listen()
wn.onkeypress(jump, 'space')
wn.onscreenclick(click)

passed = []
pipePairs = []

def construct_pipe(height):

    top = turtle.Turtle()
    top.speed(0)
    top.pu()
    top.left(90)
    top.shape('pipe2.gif')
    top.goto(width, height)   

    bottom = top.clone()
    bottom.goto(width, top.ycor() - pipeDistance - pipeHeight)
    bottom.shape('pipe.gif')

    pair = []
    pair.append(top)
    pair.append(bottom)
    pipePairs.append(pair)


dead = False
run = 0

def AI():
    if len(pipePairs) >= 1:
        # t = pipePairs[0][0]
        b = pipePairs[0][1]
        if b.ycor() + pipeDistance/2 + pipeHeight/2 > bird.ycor() + 110:
            jump()
    if bird.ycor() <= ground + 100:
        jump()

# GameLoop
class Game:
    def __init__(self):
        self.dead = False
        self.tick = 0
    
    def run(self):
        while not self.dead:
            wn.update()

            updateScore()

            self.tick += 1

            if self.tick % pipePairDistance == 0:
                construct_pipe(random.randint(pipeHeight/2, height/2))

            bird.dy += gravity
            bird.sety(bird.ycor() + bird.dy)

            if bird.ycor() <= ground + 20:
                self.dead = True
            elif bird.ycor() > height/2 - 20:
                bird.sety(height/2 - 20)
                bird.dy -= 1
            
            for pair in pipePairs:
                for pipe in pair:
                    pipe.setx(pipe.xcor() - pipeSpeed)
                    if abs(bird.xcor() - pipe.xcor()) <= pipeWidth/2 + 20 and abs(bird.ycor() - pipe.ycor()) <= pipeHeight/2 + 20:
                        self.dead = True
                        break
                if bird.xcor() > pair[0].xcor():
                    passed.append(pair[0])
                    passed.append(pair[1])
                    pipePairs.remove(pair)
                    bird.score += 1
            for p in passed:
                p.setx(p.xcor() - pipeSpeed)
                if p.xcor() < -width/2 - pipeWidth:
                    p.ht()
                    passed.remove(p)
            
            time.sleep(0.01)


        if self.dead:
            bird.color('red')
            wn.onkeypress(None, 'space')
            bird.dy += 3
            while bird.ycor() > ground + 20:
                wn.update()
                bird.dy += gravity
                bird.sety(bird.ycor() + bird.dy)
                bird.clear()
                bird.stamp()
                time.sleep(0.01)
            updateScore()
            return

# Playing Game
game = Game()
startGame = False
def start():
    global startGame
    startGame = True
# Starting game
wn.onkey(start, 'space')
# Buffer
while not startGame:
    wn.update()
    continue
# Game
game.run()

wn.update()
wn.mainloop()