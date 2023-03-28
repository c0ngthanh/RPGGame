import pygame
import random
from .spritesheet import Spritesheet
import math
import os
import csv
from .player1 import Player
from .constants import GameConstants
from .item import *
class Chest(Player):
    def __init__(self,x,y):
        super().__init__()
        self.is_open = False
        self.delete = False
        self.rect.x =x
        self.rect.y =y
        self.delay =0
        self.delay_sum = 100
        #item
        self.items = self.generate_items()
    def generate_items(self):
        items = []
        items.append(Coin(self.rect.x, self.rect.y))
        items.append(Booster(self.rect.x+100, self.rect.y))
        items.append(Shield(self.rect.x+200, self.rect.y))
        items.append(HealthPack(self.rect.x+300, self.rect.y))
        return items
    def update(self,dt,tiles):
        if self.is_open:
            self.animate()
            self.delay +=3
            if self.delay > self.delay_sum:
                self.is_open = False
                self.delete = True
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
        # self.animate()
    def animate(self):
        now = pygame.time.get_ticks()
        if self.is_open:
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                self.current_image = self.idle_frames_right[self.current_frame]
    def load_frames(self):
        my_spritesheet = Spritesheet('assets/chest/Chests.png',0.25)
        self.idle_frames_right = [my_spritesheet.parse_sprite("Chest (1).png"),my_spritesheet.parse_sprite("Chest (2).png"),
                                 my_spritesheet.parse_sprite("Chest (3).png"),my_spritesheet.parse_sprite("Chest (4).png"),
                                 my_spritesheet.parse_sprite("Chest (5).png")]
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append( pygame.transform.flip(frame,True, False) )