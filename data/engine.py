#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 14:54:02 2023

@author: matthewmartinez

Engine for Pygame. Adapted from DaFluffyPotato engine.py
"""
import math, pygame, os
from pygame.locals import *

global e_colorkey
e_colorkey = (0,0,0)

# 2D physics object 
def collisionTest(object1, object_list): # Pass a rect (object1) and list of rects to test collisions with (object_list)
    collision_list = []
    for obj in object_list:
        if object1.colliderect(obj):
            collision_list.append(obj)
    return collision_list

class physics_obj:
    
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def move(self, movement, objects): # movement is a list of x y movements. Objects are other entities
        self.x += movement[0]
        self.rect.x = int(self.x)
        
        self.y += movement[1]
        self.rect.y = int(self.y)
        
        object_hit_list = collisionTest(self.rect, objects) # Specific to Flappy bird, only possible collision with pipes
        if len(object_hit_list) != 0:
            return object_hit_list 

# Entity things
class entity:

    global animation_database
    
    def __init__(self, x, y, x_size, y_size, e_type):
        self.x = x
        self.y = y
        self.size_x = x_size
        self.size_y = y_size
        self.obj = physics_obj(x, y, x_size, y_size)
        self.animation = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.image = None 
        self.offset = [0, 0]
        self.rotation = 0
        self.type = e_type
        self.action_timer = 0
        self.action = '' # If set to 'click', start the action timer. This will change rotation of bird going up/down
        self.set_action('wing_flap') # overall action for the entity
        self.entity_data = {}
        self.alpha = None
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.obj.x = x
        self.obj.y = y 
        self.obj.rect.x = x
        self.obj.rect.y = y
        
    def move(self, momentum, objects):
        collisions = self.obj.move(momentum, objects)
        self.x = self.obj.x
        self.y = self.obj.y
        return collisions
    
    def rect(self):
        return pygame.Rect (self.x, self.y, self.x_size, self.y_size)
    
    def set_flip(self, boolean):
        self.flip = boolean
        
    def set_animation_tags(self, tags):
        self.animation_tags = tags
        
    def set_animation(self, sequence):
        self.animation = sequence
        self.animation_frame = 0
        
    def set_action(self,action_id,force=False):
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0
    
    def get_entity_angle(self, entity_2): # Angle with respect to another entity
        x1 = self.x + int(self.x_size / 2) # Center x of self
        y1 = self.y + int(self.y_size / 2) # Center y of self
        x2 = entity_2.x + int(entity_2.x_size / 2)
        y2 = entity_2.y + int(entity_2.y_size / 2)
        angle = math.atan((y2-y1) / (x2-x1))
        if x2 < x1:
            angle += math.pi # Flip by 180 degrees if entity_2 to left of self
        return angle
    
    def get_center(self):
        center_x =  self.x + int(self.x_size / 2)
        center_y = self.y + int(self.y_size / 2)
        return [center_x, center_y]
    
    def clear_animation(self):
        self.animation = None
        
    def set_image(self, image):
        self.image = image
        
    def set_offset(self, offset):
        self.offset = offset
    
    def set_frame(self, amount):
        self.animation_frame = amount
        
    def handle(self):
        self.action_timer += 1
        self.change_frame(1)
        
    def change_frame(self, amount): # A little comfused about how this works. Unpack this at some point
        self.animation_frame += amount
        if self.animation_frame != None:
            while self.animation_frame < 0:
                if 'loop' in self.animation_tags:
                    self.animation_frame += len(self.animation)
                else:
                    self.animation = 0
            while self.animation_frame >= len(self.animation):
                if 'loop' in self.animation_tags:
                    self.animation_frame -= len(self.animation)
                else:
                    self.animation_frame = len(self.animation) - 1
                
    def get_current_img(self):
        if self.animation == None:
            if self.image != None:
                return flip(self.image, self.flip)
            else:
                return None
        else:
            return flip(animation_database[self.animation[self.animation_frame]], self.flip)
        
    def get_drawn_img(self):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image, self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]], self.flip).copy()
        
        if image_to_render != None:
            center_x = image_to_render.get_width() / 2
            center_y = image_to_render.get_height() / 2
            image_to_render = pygame.transform.rotate(image_to_render, self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            return image_to_render, center_x, center_y
        
    def display(self, surface, scroll=[0,0]):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image, self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]], self.flip).copy()
        
        if image_to_render != None:
            center_x = image_to_render.get_width() / 2
            center_y = image_to_render.get_height() / 2
            image_to_render = pygame.transform.rotate(image_to_render, self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            blit_center(surface, image_to_render, (int(self.x) - scroll[0] + self.offset[0] + center_x, int(self.y) - scroll[1] + self.offset[1] + center_y))
        
def simple_entity(x, y, e_type):
    return entity(x, y, 1, 1, e_type)      

def flip(img, boolean=True):
    return pygame.transform.flip(img, boolean, False)

def blit_center(surface, surface_2, pos): # Surface_2 is object to blit
    x = int(surface_2.get_width() / 2)
    y = int(surface_2.get_height() / 2)
    surface.blit(surface_2, (pos[0] - x, pos[1] - y))
    
# Animation stuff
global animation_database
animation_database = {}

global animation_higher_database
animation_higher_database = {}

def animation_sequence(sequence,base_path,colorkey=(255,255,255),transparency=255):
    global animation_database
    
    if base_path[-1] != '/': # Ensure that the supplied path ends in a /
        base_path += '/'
        
    result = []
    for frame in sequence:
        image_id = base_path + base_path.split('/')[-2] + '_' + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert()
        image.set_colorkey(colorkey)
        image.set_alpha(transparency)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result

def get_frame(ID):
    global animation_database
    return animation_database[ID]

def load_animations(path):
    global animation_database
    f = open(path + 'entity_animations.txt', 'r') # This text file contains info on every animation. Each line is animation info such as directory, frame durations, and loop or not
    data = f.read()
    f.close()
    
    for animation in data.split('\n'):
        sections = animation.split()
        anim_path = sections[0]
        entity_info = anim_path.split('/')
        entity_type = entity_info[0] # i.e. directories may be setup like player/idle, player/run, etc
        if len(entity_info) > 1: # If there's mroe than 1 type of animation per entity
            animation_id = entity_info[1]
        timings = sections[1].split(';')
        tags = sections[2].split(';')
        sequence = []
        n = 0
        for timing in timings:
            sequence.append([n,int(timing)])
            n += 1
        anim = animation_sequence(sequence,path + anim_path,e_colorkey)
        if entity_type not in animation_higher_database:
            animation_higher_database[entity_type] = {}
        animation_higher_database[entity_type][animation_id] = [anim.copy(),tags]
        

def change_action(action_var, frame, new_action):
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var, frame


