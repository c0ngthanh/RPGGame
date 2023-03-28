import pygame
from .constants import GameConstants
import random
from .spritesheet import Spritesheet
import os
import csv

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.load_frames()
        self.current_image = self.running_frames_right[0]
        self.current_frame = 0
        self.last_updated = 0
        # self.image.fill((255, 0, 255))
        self.rect = self.attacking_frames_left[0].get_rect()
        self.position, self.velocity = pygame.math.Vector2(x, y), pygame.math.Vector2(0, 0)
        self.gravity, self.friction = 0.35, -0.12
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.on_ground = False

        # Attributes
        self.health = 50
        self.max_health = 50
        self.state = 'moving left'
        self.attack_range = 50
        self.attack_cooldown = 1000  # Attack cooldown in milliseconds
        self.last_attack = 0

    def update(self, dt, tiles, player,csv):
        self.handle_ai(dt, player,tiles,csv)
        self.animate()
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)
        # self.test(tiles,csv)

    def handle_ai(self, dt, player,tiles,csv):
        distance_to_player = self.position.x - player.position.x

        # Chase the player if they are within 250 units
        if -100 < distance_to_player < 100:
            if distance_to_player > 0:
                self.state = 'moving left'
                self.acceleration.x = -0.1
            elif distance_to_player < 0:
                self.state = 'moving right'
                self.acceleration.x = 0.1

            # Attack the player if they are within the attack range and the attack is not on cooldown
            if distance_to_player < self.attack_range and pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                self.state = 'attack'
                self.attack(player)
        
        else:
            # Randomly choose a direction to move if the player is not within range
            check = self.test(tiles,csv)
            # add = random.choice([-0.01, 0, 0.01])
            if self.state == 'moving left' and self.on_ground:
                if check != 'LEFT':
                    self.position.x -= 0.2
                else:
                    self.state = 'moving right'
            elif self.state == 'moving right' and self.on_ground:
                if check != 'RIGHT':
                    self.position.x += 0.2
                else: 
                    self.state = 'moving left'
    def test(self,tiles,csv):
        map = csv
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            y = int(tile.rect.y/32)
            x = int(tile.rect.x/32)
            # print(tile.rect.x)
            if map[y][x-1] == '-1' and self.rect.x == tile.rect.x:
                # print(map[y][x])
                return 'LEFT'
            elif map[y-1][x-1] != '-1' and self.rect.x == tile.rect.x:
                # print(map[y][x])
                return 'LEFT'
            elif map[y][x+1] == '-1' and self.rect.x == tile.rect.x:
                # print(map[y][x])
                return 'RIGHT'
            elif map[y-1][x+1] != '-1' and self.rect.x == tile.rect.x:
                # print(map[y][x])
                return 'RIGHT'
        return 'NONE'
            
    def attack(self, player):
        player.health -= 10
        if player.health < 0:
            player.health = 0
        self.last_attack = pygame.time.get_ticks()

    def horizontal_movement(self, dt):
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(1)
        self.position.x += self.velocity.x * dt
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .2) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisions_x(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
            elif self.velocity.x < 0:
                self.position.x = tile.rect.right
            self.rect.x = self.position.x

    def check_collisions_y(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.velocity.y = 0
                self.position.y = tile.rect.top
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
            self.rect.bottom = self.position.y

    def draw_health_bar(self, surface):
        health_bar_width = self.rect.width
        health_bar_height = 5
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - health_bar_height - 2

        health_bar_filled = int((self.health / self.max_health) * health_bar_width)

        health_bar_bg = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        health_bar_fill = pygame.Rect(health_bar_x, health_bar_y, health_bar_filled, health_bar_height)

        pygame.draw.rect(surface, (100, 100, 100), health_bar_bg)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_fill)
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'moving right' or self.state == 'moving left':
            if now - self.last_updated > 50:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.running_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.running_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.running_frames_right[self.current_frame]
        elif self.state == 'attack':
            # print(self.current_frame)
            if now - self.last_updated > 30:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attacking_frames_left)
                if self.state == 'attack':
                    self.current_image = self.attacking_frames_left[self.current_frame]
                # elif self.state == 'attack' and not self.FACING_LEFT:
                #     self.current_image = self.attacking_frames_right[self.current_frame]
    def load_frames(self):
        my_spritesheet = Spritesheet('assets/zombie/zombie.png',10)
        self.attacking_frames_right = [my_spritesheet.parse_sprite("Attack (1).png"),my_spritesheet.parse_sprite("Attack (2).png"),
                                     my_spritesheet.parse_sprite("Attack (3).png"),my_spritesheet.parse_sprite("Attack (4).png"),
                                     my_spritesheet.parse_sprite("Attack (5).png"),my_spritesheet.parse_sprite("Attack (6).png"),
                                     my_spritesheet.parse_sprite("Attack (7).png"),my_spritesheet.parse_sprite("Attack (8).png")]
        self.running_frames_right = [my_spritesheet.parse_sprite("Walk (1).png"),my_spritesheet.parse_sprite("Walk (2).png"),
                                     my_spritesheet.parse_sprite("Walk (3).png"),my_spritesheet.parse_sprite("Walk (4).png"),
                                     my_spritesheet.parse_sprite("Walk (5).png"),my_spritesheet.parse_sprite("Walk (6).png"),
                                     my_spritesheet.parse_sprite("Walk (7).png"),my_spritesheet.parse_sprite("Walk (8).png"),
                                     my_spritesheet.parse_sprite("Walk (9).png"),my_spritesheet.parse_sprite("Walk (10).png")]
        self.dead_frames_right =    [my_spritesheet.parse_sprite("Dead (1).png"),my_spritesheet.parse_sprite("Dead (2).png"),
                                     my_spritesheet.parse_sprite("Dead (3).png"),my_spritesheet.parse_sprite("Dead (4).png"),
                                     my_spritesheet.parse_sprite("Dead (5).png"),my_spritesheet.parse_sprite("Dead (6).png"),
                                     my_spritesheet.parse_sprite("Dead (7).png"),my_spritesheet.parse_sprite("Dead (8).png"),
                                     my_spritesheet.parse_sprite("Dead (9).png"),my_spritesheet.parse_sprite("Dead (10).png"),
                                     my_spritesheet.parse_sprite("Dead (11).png"),my_spritesheet.parse_sprite("Dead (12).png")]
        self.dead_frames_left = []
        for frame in self.dead_frames_right:
            self.dead_frames_left.append( pygame.transform.flip(frame,True, False) )
        self.running_frames_left = []
        for frame in self.running_frames_right:
            self.running_frames_left.append(pygame.transform.flip(frame, True, False))
        self.attacking_frames_left = []
        for frame in self.attacking_frames_right:
            self.attacking_frames_left.append( pygame.transform.flip(frame,True, False) )