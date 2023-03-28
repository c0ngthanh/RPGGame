import pygame
import json

class Spritesheet:
    def __init__(self, filename,scale):
        self.filename = filename
        self.scale = scale
        self.sprite_sheet = pygame.image.load(filename)
        self.width,self.height = self.sprite_sheet.get_rect().width/scale,self.sprite_sheet.get_rect().height/scale
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,(self.width,self.height))
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"]/self.scale, sprite["y"]/self.scale, sprite["w"]/self.scale, sprite["h"]/self.scale
        image = self.get_sprite(x, y, w, h)
        return image