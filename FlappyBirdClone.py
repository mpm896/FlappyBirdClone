# -*- coding: utf-8 -*-
"""
Flappy bird clone!

@author: Matt Martinez 
"""
import sys, random
import pygame
from pygame.locals import *
import data.engine as e
import data.UI.UI as UI

#GLOBAL VARS    
WHITE               = (255, 255, 255)
BLACK               = (0, 0, 0)
FPS                 = 30
PIPE_SPEED          = 3

def terminate():
    pygame.quit()
    sys.exit()
  
def movePipes(bird, pipe_pair, pointSoundCount, score):
    """
    ARGS: bird - bird object
          pipe_pair - 2-d list of pipe objects
          pointSoundCount - flg variable to ensure sound only plays once
          score - int
    """
    score_point = False
    # Point and sound for FIRST pipe of the game
    if pipe_pair[0][0].rect.right < bird.obj.rect.left and pointSoundCount == 0:
        pointSound.play()
        pointSoundCount = 1
        score += 1

    for i, obj in enumerate(pipe_pair):
        if i == 0:
            obj[0].rect.x -= PIPE_SPEED
            obj[1].rect.x -= PIPE_SPEED

            if obj[0].rect.right < 0:
                pipe_pair.append([e.physics_obj(WINDOW_WIDTH, WINDOW_HEIGHT - pipe_image.get_height(), pipe_image.get_width(), pipe_image.get_height()),
                                e.physics_obj(WINDOW_WIDTH, 0, pipe_image.get_width(), pipe_image.get_height())])
                pipe_pair.pop(0)
                pointSoundCount = 0

        if i == 1: 
            if obj[0].rect.right < bird.obj.rect.left and pointSoundCount == 0:
                pointSoundCount = 1
                pointSound.play()
                score += 1
                score_point = True

        if i > 0:
            if pipe_pair[i-1][0].rect.x < (WINDOW_WIDTH / 2):
                obj[0].rect.x -= PIPE_SPEED
                obj[1].rect.x -= PIPE_SPEED
            elif obj[0].rect.x != WINDOW_WIDTH:
                obj[0].rect.x -= PIPE_SPEED
                obj[1].rect.x -= PIPE_SPEED
    
    return score, pointSoundCount

# Initialize the game
pygame.init()
FONT                = pygame.font.SysFont(None, 48)
SUBFONT             = pygame.font.SysFont(None, 32)
mainClock = pygame.time.Clock()

# Because there is a full background image, set window height and image to background image
background_image = pygame.image.load('data/Game_Objects/background.png')
WINDOW_WIDTH = background_image.get_width() * 1.5
WINDOW_HEIGHT = background_image.get_height()

windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Flappy Bird clone!')

# Load sounds
dieSound = pygame.mixer.Sound('data/SoundEffects/die.wav')
hitSound = pygame.mixer.Sound('data/SoundEffects/hit.wav')
pointSound = pygame.mixer.Sound('data/SoundEffects/point.wav')
swooshSound = pygame.mixer.Sound('data/SoundEffects/swoosh.wav')
wingSound = pygame.mixer.Sound('data/SoundEffects/wing.wav')

# Load sprites and images
ground_image = pygame.image.load('data/Game_Objects/base.png').convert()
pipe_image = pygame.image.load('data/Game_Objects/pipe.png').convert()
pipe_image_flipped = pygame.transform.flip(pipe_image.copy(), False, True)

global animation_database, animation_frames

# Bird animations and object
e.load_animations('data/Game_Objects/') # Full wing flap every 15 frames. At 60 FPS, 4 flaps per second

# Pipe object
pipe_width = pipe_image.get_width()
pipe_height = pipe_image.get_height()

# Load number images
number_catalog = []
for i in range(10):
    number_catalog.append(pygame.image.load('data/UI/Numbers/' + str(i) +'.png'))

while True: # Game startup screen
    UI.gameStartup(windowSurface, pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT)))
   
    score = 0
    pointSoundCount = 0 # Variable to ensure the sound for scoring a point only plays once when you pass a pipe

    bird = e.entity(50, WINDOW_HEIGHT / 2, 34, 24, 'bird') # Get actual dimensions of images for bird animations   
    pipe_pair = []
    for i in range(3):
        pipe_pair.append([e.physics_obj(WINDOW_WIDTH, WINDOW_HEIGHT - pipe_image.get_height(), pipe_image.get_width(), pipe_image.get_height()), 
                          e.physics_obj(WINDOW_WIDTH, 0, pipe_image.get_width(), pipe_image.get_height())])
    
    # Initialize jumping/falling momentum
    vertical_momentum = 0
    
    UI.waitForStartClick()
    while True: # Main game loop
        player_movement = [0, 0] # Set the amount moved to 0 each frame
        
        # Events. Main events are spacebar and click for the jump, and clicking certain boxes on the screen
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_SPACE: # Jump if space bar or left mouse button clicked
                    vertical_momentum = -9
                    wingSound.play()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: # 1 is left mouse click
                vertical_momentum = -9
                wingSound.play()
        
        # Bird gravity and rotation if jumping/falling
        if vertical_momentum <= -5:
            bird.rotation = 30
        else:
            bird.rotation -= 4
            if bird.rotation < -45:
                bird.rotation = -45
        
        # Move bird and update position        
        player_movement[1] += vertical_momentum
        collisions = bird.move(player_movement, [pipe for pair in pipe_pair for pipe in pair])
        bird.change_frame(1)
        
        if collisions:
            vertical_momentum = 0
            hitSound.play()
            UI.displayGameOver(windowSurface)
            pygame.display.update()
            break
        
        # Collision with top or bottom
        if bird.obj.rect.bottom > WINDOW_HEIGHT or bird.obj.rect.top < 0:
            vertical_momentum = 0
            hitSound.play()
            UI.displayGameOver(windowSurface)
            pygame.display.update()
            break
        
        vertical_momentum += 0.9 # Increase this so always falling
        if vertical_momentum > 10:
            vertical_momentum = 10
        
        # Display backgorund
        windowSurface.blit(pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT)), background_image.get_rect())
        
        # Set pipe position
        for pair in pipe_pair:
            if pair[0].rect.x == WINDOW_WIDTH:
                pair[0].rect.top = random.randint(WINDOW_HEIGHT-pair[0].height, WINDOW_HEIGHT - 110)
                pair[1].rect.bottom = pair[0].rect.top - 110
        """
        # Point and sound for FIRST pipe of the game
        if pipe_pair[0][0].rect.right < bird.obj.rect.left and pointSoundCount == 0:
            pointSound.play()
            pointSoundCount = 1
            score += 1
        """
        
        score, pointSoundCount = movePipes(bird, pipe_pair, pointSoundCount, score)

        # Display pipes on screen. When this was in the loop for moving pipes,
        # the middle pipe would flash when the left one disappeared
        for obj in pipe_pair:
            windowSurface.blit(pipe_image, obj[0].rect)
            windowSurface.blit(pipe_image_flipped, obj[1].rect)

        UI.displayScore(score, number_catalog, windowSurface, WINDOW_WIDTH)

        bird.display(windowSurface)
        pygame.display.update()
        mainClock.tick(FPS)

        
    UI.waitForKeyInput()

    
