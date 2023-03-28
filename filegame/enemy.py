import pygame
from .constants import GameConstants
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(x, y), pygame.math.Vector2(0, 0)
        self.gravity, self.friction = 0.35, -0.12
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.on_ground = False

        # Attributes
        self.health = 200
        self.max_health = 200
        self.ai_state = 'idle'
        self.attack_range = 50
        self.attack_cooldown = 1000  # Attack cooldown in milliseconds
        self.last_attack = 0

    def update(self, dt, tiles, player):
        self.handle_ai(dt, player)
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)

    def handle_ai(self, dt, player):
        distance_to_player = self.position.distance_to(player.position)

        # Chase the player if they are within 250 units
        if -150 < distance_to_player < 150:
            if distance_to_player > 0:
                self.acceleration.x = -0.1
            elif distance_to_player < 0:
                self.acceleration.x = 0.1

            # Attack the player if they are within the attack range and the attack is not on cooldown
            if distance_to_player < self.attack_range and pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                self.attack(player)
        else:
            # Randomly choose a direction to move if the player is not within range
            self.acceleration.x = random.choice([-0.1, 0, 0.1])
            
    def attack(self, player):
        player.health -= 10
        if player.health < 0:
            player.health = 0
        self.last_attack = pygame.time.get_ticks()

    def horizontal_movement(self, dt):
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(2)
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
