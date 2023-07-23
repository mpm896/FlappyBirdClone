#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 15:00:14 2023

@author: matthewmartinez

User interface stuff
"""
import pygame, sys
from pygame.locals import *

def terminate():
    pygame.quit()
    sys.exit()

def gameStartup(surface, background=None):
    gameStartImage = pygame.image.load('data/UI/message.png')
    imageRect = gameStartImage.get_rect()
    imageRect.center = (surface.get_width() / 2, surface.get_height() / 2)
    if background:
        backgroundRect = background.get_rect()
        surface.blit(background, backgroundRect)
    surface.blit(gameStartImage, imageRect)    
    pygame.display.update()

def displayGameOver(surface): # Display the game over screen when pipe or ground hit. Might need to pass the score
    gameOverImage = pygame.image.load('data/UI/gameover.png')
    imageRect = gameOverImage.get_rect()
    imageRect.center = (surface.get_width() / 2, surface.get_height() / 2)
    surface.blit(gameOverImage, imageRect)   

def drawText(text, font, surface, x, y):
    textObj = font.render(text, 1, )
    text_rect = textObj.get_rect()
    text_rect.center = (x, y)
    surface.blit(textObj, text_rect)
    
def waitForKeyInput():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                return # Return is here because it only returns if keydown/up event occurs
            
def waitForStartClick():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
            if event.type == MOUSEBUTTONDOWN and event.button == 1: # 1 is left mouse buttn
                return
            
def displayScore(score, number_images, surface, WINDOW_WIDTH):  
    """
    ARGS: score - int 
          number_images - list of images
          surface - main surface to blit images on
          WINDOW_SIZE - tuple of width and height
    """
    score_rect_width = 0
    numbers_to_render = []
    number_rects = []
    for i in range(len(str(score))):
        numbers_to_render.append(number_images[int(str(score)[i])])
        number_rects.append(numbers_to_render[i].get_rect())
        score_rect_width += number_rects[i].width
    
    score_rect = pygame.Rect((WINDOW_WIDTH / 2) - (score_rect_width / 2), 50, score_rect_width, number_rects[0].height)
    
    for i, number in enumerate(numbers_to_render):
        x_pos = score_rect.left + ((i / len(numbers_to_render)) * score_rect_width)
        surface.blit(numbers_to_render[i], (x_pos, 50))
        