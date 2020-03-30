import turtle
import random
import time

from flappy_network import NeuralNetwork
from flappy_matrix import Matrix

width = 475
height = 650

# Pipe Variables
pipePairDistance = 100
pipeDistance = 125
pipeHeight = 400
pipeWidth = 80
pipeSpeed = 3

frameRate = 1

# Genetic Algorithm
population = []
saved = []
populationSize = 300
generationNumber = 1
resetRate = 1
score = 0
only_show_best = False

# Setup Screen
wn = turtle.Screen()
wn.title('Flappy Bird')
wn.setup(width, height)
wn.bgcolor('light blue')
wn.bgpic('flappybg.gif')
wn.tracer(0)

# Shapes and Pictures
wn.register_shape('pipe', ((-pipeWidth/2, pipeHeight/2), (pipeWidth/2, pipeHeight/2), (pipeWidth/2, -pipeHeight/2), (-pipeWidth/2, -pipeHeight/2)))
wn.register_shape('bird.gif')
wn.register_shape('pipe.gif')
wn.register_shape('pipe2.gif')

# Floor Setup
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

# Bird Constructor Function
def Bird(brain):
    bird = turtle.Turtle()
    bird.shape('bird.gif')
    bird.speed(0)
    bird.pu()
    bird.setpos(-50, 0)
    bird.score = 0
    bird.fitness = 0
    bird.dead = False
    if brain: bird.brain = brain.copy()
    else: bird.brain = NeuralNetwork(5, 1, 1)
    bird.dy = 0
    return bird

# Generating Population
for i in range(populationSize): 
    newBird = Bird(False)
    population.append(newBird)
    

def nextGeneration():
    global population, saved
    population = []
    calculateFitness()
    for _ in range(populationSize):
        population.append(pickOne())
    saved = []

def pickOne():
    global saved
    index = 0
    r = random.random()
    while r > 0:
        r = r - saved[index].fitness
        index += 1
    index -= 1
    bird = saved[index]
    child = Bird(bird.brain)
    child.brain.mutate(0.1)
    if random.randint(0, 100) == resetRate:
        child.brain = NeuralNetwork(5, 1, 1)
    return child

def calculateFitness():
    sum = 0
    for bird in saved:
        sum += bird.score
    for bird in saved:
        bird.fitness = bird.score / sum

scorer = turtle.Turtle()
scorer.speed(0)
scorer.ht(); scorer.pu()
scorer.color('black')
scorer.goto(0, height/2 - 120)

writer = scorer.clone()
writer.goto(-width/2 + 10, height/2 - 25)


def updateScore():
    global score, generationNumber
    scorer.clear(); writer.clear()
    scorer.write(score, move=False, align="center", font=("Courier", 30, "bold"))
    writer.write('Gen: ' + str(generationNumber), move=False, align="left", font=("Arial", 15, "bold"))


gravity = -0.4

def jump(bird):
    bird.dy += 10

def dump():
    d = population[0].brain.serialize()
    file = open('data.txt', 'w+')
    for val in d:
        file.write(str(val) + '\n')
    file.close()

def speedUp():
    global frameRate
    frameRate += 2

def slowDown():
    global frameRate
    if frameRate - 2 > 0:
        frameRate -= 2
    else: frameRate = 1


wn.listen()
wn.onkey(dump, 's')

wn.onkeypress(speedUp, 'Right')
wn.onkeypress(slowDown, 'Left')

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


# bird = population[0]
# bird.brain.weights_ho.data = [[-0.7467888815839512]]
# bird.brain.weights_ih.data = [[0.9228352829621123, -0.8782787783493267, -0.1889264415851699, 0.21969669032961048, 0.8118099841735795]]
# bird.brain.bias_h.data = [[0.1322983423031021]]
# bird.brain.bias_o.data = [[0.3087143504140357]]


dead = False
run = 0

# GameLoop
while True:

    if run % frameRate == 0:
        wn.update()

    updateScore()

    if run % pipePairDistance == 0:
        construct_pipe(random.randint((height/2) - (pipeHeight/2), pipeHeight + pipeDistance + pipeHeight/2 - height/2))

    run += 1

    for pair in pipePairs:
        for pipe in pair:
            pipe.setx(pipe.xcor() - pipeSpeed)
        if -50 > pair[0].xcor() + pipeWidth/2:
                passed.append(pair[0])
                passed.append(pair[1])
                pipePairs.remove(pair)
                # bird.score += 1
                score += 1
    for p in passed:
        p.setx(p.xcor() - pipeSpeed)
        if p.xcor() < -width/2 - pipeWidth:
            p.ht()
            passed.remove(p)
            p.goto(1000, 1000)
    
    # Finding best player
    if only_show_best:
        best_score = -1
        best_player = None
        for bird in population:
            if bird.score > best_score:
                best_score = bird.score
                best_player = bird
    
    # Moving population
    for bird in population:
        bird.score += 1

        # Only showing best player
        if only_show_best:
            if bird == best_player: bird.st()
            else: bird.ht()

        # Player Network inputs (normalized)
        
        inputs = [
            bird.ycor() / (height/2),
            (pipePairs[0][0].ycor() - pipeHeight/2) / (height/2),
            (pipePairs[0][1].ycor() + pipeHeight/2) / (height/2),
            (pipePairs[0][0].xcor() + pipeWidth/2) / (width/2),
            bird.dy / 10
        ] 

        output = bird.brain.predict(inputs)

        if output[0] > 0.5:
            jump(bird)

        bird.dy += gravity
        bird.sety(bird.ycor() + bird.dy)

        if bird.ycor() <= ground + 20:
            bird.dead = True
        elif bird.ycor() > height/2 - 20:
            # bird.sety(height/2 - 20)
            # bird.dy -= 1
            bird.dead = True
        
        for pair in pipePairs:
            for pipe in pair:
                if abs(bird.xcor() - pipe.xcor()) <= pipeWidth/2 + 20 and abs(bird.ycor() - pipe.ycor()) <= pipeHeight/2 + 10:
                    bird.dead = True
                    break 

        if bird.dead:
            population.remove(bird)
            saved.append(bird)
            bird.ht()
            bird.goto(10000, 10000)
    
    # Resetting Game
    if len(population) == 0:
        nextGeneration()
        score = 0
        generationNumber += 1
        for pair in pipePairs:
            for pipe in pair:
                pipe.ht()
        for pipe in passed:
            pipe.ht()
        passed = []
        pipePairs = []
        run = 0
        time.sleep(0.5)

    # time.sleep(0.01)

wn.update()
wn.mainloop()