import pygame  # install the pygame package for the project
import random
import math
from pygame import mixer



pygame.init()  # initiate the pygame package so that we can use its features

# The next step is to create the screen for the game in which it could be played
# This is done by creating a screen variable using pygame


screen = pygame.display.set_mode((1024, 576))  # specify size in bracket

# inorder that the screen remains active till game is not closed we create an infinite loop which stops only when
# quit event is detected

# to add a title(caption) and icon to window
pygame.display.set_caption("Space Invader")
"""
to add an image download the image and store it in project file in png format usually for icon prferred is 32X32 size


to load image in project use this 
pygame.image.load("name of image ")
then to set as icon use 
pygame.display.set_icon("name of image")
"""
# loading the background image
background = pygame.image.load('space.png')
# specify number of enemies and store them in a list
number_of_enemies = 12


EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
# load the image of the spaceship and enemies and bullets
bulletImg = pygame.image.load('bullet.png')

playerImg = pygame.image.load('spaceship.png')
# specify the coordinates where the image should be drawn remember x positive left to right and y positive up to down
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
gameOverfont = pygame.font.Font('freesansbold.ttf', 120)

textX = 10
textY = 10

# enemy
for i in range(number_of_enemies):
    EnemyImg.append(pygame.image.load('alien.png'))
    EnemyX.append(random.randint(0, 940))
    EnemyY.append(random.randint(50, 300))
    EnemyX_change.append(1.0)
    EnemyY_change.append(0.09)

# player
playerX = 500
playerY = 460
playerX_change = 0  # a variable to implement the corresponding change in x when a key is pressed from key board

# bullet
# define the global initial state of bullet
bullet_state = 'ready'
bulletX = 0
bulletY = 450
bullet_change = 3


# create a function that draws the image of the spaceship on the screen
def player(x, y):  # modify player function from player() to player(x,y)
    screen.blit(playerImg, (x, y))


# a function that draws image of enemy on screen
def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


# function to fire bullet whenever called
def bullet_fire(x, y):
    global bullet_state
    bullet_state = 'fired'
    screen.blit(bulletImg, (x + 16, y))


# blit means to draw pass name of image and the coordinates

# a function to check whether there is a collision or not
def is_collision(EnemyY, EnemyX, bulletY, bulletX, ):
    distance = math.sqrt((math.pow(EnemyY - bulletY, 2)) + (math.pow(EnemyX - bulletX, 2)))
    if distance < 27:
        return True
    else:
        return False


# function to display score on screen
def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_game_over():

    over = gameOverfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (450, 200))



def game_over(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyY - playerY, 2)) + (math.pow(enemyX - playerX, 2)))
    if distance < 50:
        return True
    else:
        return False


running = True
# anything that you want to keep persistent throughout the game should be written in the infinite loop below
while running:

    # to set a background color write
    # set background image

    screen.fill((80, 73, 125))
    screen.blit(background, (0, 0))

    # playerY -= 0.09 just a test to see the spaceship move

    # we check through all events whether any of it happened or not
    for event in pygame.event.get():  # loop through all event
        if event.type == pygame.KEYDOWN:  # Key down event is when we press a key
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state is 'ready':
                
                bulletX = playerX
                bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # Key up event is when we stop pressing a key
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.QUIT:
            running = False
    for i in range(number_of_enemies):
        EnemyX[i] += EnemyX_change[i]
        EnemyY[i] += EnemyY_change[i]
        if EnemyX[i] < 0:
            EnemyX[i] = 0
            EnemyX_change[i] = 0.7
        if EnemyX[i] > 960:
            EnemyX[i] = 960
            EnemyX_change[i] = -0.7

        if game_over(EnemyY[i], EnemyX[i], playerY, playerX):


            for j in range(number_of_enemies):
                EnemyX[j] = 1500
                EnemyY[j] = 2000
            break

        if is_collision(EnemyY[i], EnemyX[i], bulletY, bulletX):
            bulletY = 450
            bullet_state = 'ready'
            score_value += 1
            EnemyX[i] = random.randint(0, 940)
            EnemyY[i] = 0

        Enemy(EnemyX[i], EnemyY[i], i)

    # checking that bullet remains persistent after firing
    if bullet_state is 'fired':
        bullet_fire(bulletX, bulletY)
        bulletY -= bullet_change


    if bulletY <= 0:
        bulletY = 450
        bullet_state = 'ready'
    playerX += playerX_change

    # we now create boundaries
    # enemies

    # players
    if playerX < 0:
        playerX = 0
    if playerX > 960:
        playerX = 960

        # call player function to draw image
    player(playerX, playerY)

    show_score(textX, textY)
    # call the enemy function

    # to update the display continuously write this
    pygame.display.update()

