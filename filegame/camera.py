import pygame
vec = pygame.math.Vector2
from .player import Player
from .constants import GameConstants
class Camera:
    def __init__(self,player :Player):
        self.player = player
        self.x = 0
        self.y = 0
        self.width = GameConstants.BACKGROUNWIDTH
    def scroll(self):
        x_camera = self.player.rect.x - (GameConstants.GAMEWIDTH/2 - self.player.rect.w/2)
        if x_camera < 0:
            x_camera = 0
        if x_camera + GameConstants.GAMEWIDTH > self.width:
            x_camera = self.width - GameConstants.GAMEWIDTH
        self.x = -x_camera
            