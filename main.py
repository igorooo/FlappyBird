import pygame as pg
import time
from random import randint

black = (0,0,0)
white = (255,255,255)
RESOLUTION = (800,400)
GAP_LVL = 2.5
BLOCK_SPEED = 3
FALLING_LVL = 3
RISE_LVL = -4   #neative number needed

pg.init()
surface = pg.display.set_mode(RESOLUTION)
img = pg.image.load('Helicopter.png')
imgSize = img.get_rect().size
pg.display.set_caption('Helicopter')
clock = pg.time.Clock()


def replay_or_quit():
    for event in pg.event.get([pg.KEYDOWN, pg.KEYUP, pg.QUIT]):
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            continue

        return event.key
    return None

def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def msgSurface(text):
    smallText = pg.font.Font('freesansbold.ttf', 20)
    largeText = pg.font.Font('freesansbold.ttf', 150)

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = RESOLUTION[0]/ 2, RESOLUTION[1]/2
    surface.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = RESOLUTION[0]/ 2, (RESOLUTION[1]/2 +100)
    surface.blit(typTextSurf, typTextRect)

    pg.display.update()
    time.sleep(1)

    while replay_or_quit() == None:
        time.sleep(0.5)
        clock.tick()

    game()


def gameOver():
    msgSurface("Kaboom!")

def helicopter( x , y , image):
    surface.blit(image, (x,y))

def blocks(x_block, y_block, block_width, block_height, gap):
    pg.draw.rect(surface, white, [x_block, y_block, block_width, block_height])
    pg.draw.rect(surface, white, [x_block, y_block + block_height + gap, block_width, RESOLUTION[1]])


def game():
    x = 150
    y = 200
    y_move = 0  #STARTING FALLING SPEED
    game_over = False

    x_block = RESOLUTION[0]
    y_block = 0

    block_width = 75
    block_height = randint(10,RESOLUTION[1]/2)
    gap = imgSize[1] * GAP_LVL  # GAP HERE
    
    block_move = BLOCK_SPEED

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    y_move = RISE_LVL

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    y_move = FALLING_LVL
        
        y += y_move

        if(y > RESOLUTION[1] - imgSize[1] or y < 0):
            gameOver()

        if x_block < (-1 * block_width):
            x_block = RESOLUTION[0]
            block_height = randint(0, RESOLUTION[1]/2)

        if x + imgSize[0] > x_block:
            if x < x_block + block_width:
                print("possible bounds")
                if y < block_height:
                    print('Y crossover upper')
                    if x - imgSize[0] < block_width + x_block:
                        print("game over hit upper")
                        gameOver()
            if y + imgSize[1] > block_height + gap:
                print("Y cross lower")
                if x < block_width + x_block:
                    print("game over hit lower")
                    gameOver()


        surface.fill(black)
        helicopter(x,y,img)

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        pg.display.update()
        clock.tick(100)


game()
pg.quit()
quit()







