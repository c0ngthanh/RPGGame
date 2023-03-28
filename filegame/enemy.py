import pygame
from .constants import GameConstants
import random
from .spritesheet import Spritesheet
import math
import os
import csv


class EnemyFireBall():
    def __init__(self, scale, direction):
        self.load_frames(scale)
        self.x_camera = 0
        self.rect = self.frames_right[0].get_rect()
        self.current_frame = 0
        self.last_updated = 0
        self.current_image = self.frames_right[0]
        self.shoot = False
        self.direction = direction  # 'left', 'right', 'up', 'down'
        self.fireball_speed = 1.2

    def checkcollision(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.shoot = False
                return

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 10  # Adjust the damage value as needed
            self.shoot = False
            return True
        return False

    def draw(self, display, x, y, tiles, player):
        self.update(x, self.direction, player)
        self.checkcollision(tiles)
        display.blit(self.current_image, (self.rect.x + x, self.rect.y + y))

    def update(self, x, direction, player):

        self.x_camera = x
        if direction == 'right':
            self.rect.x += self.fireball_speed
            if self.rect.x > GameConstants.GAMEWIDTH - x:
                self.shoot = False
        elif direction == 'left':
            self.rect.x -= self.fireball_speed
            if self.rect.x < -x:
                self.shoot = False
        elif direction == 'up':
            self.rect.y -= self.fireball_speed
            if self.rect.y < -x:
                self.shoot = False
        elif direction == 'down':
            self.rect.y += self.fireball_speed
            if self.rect.y > GameConstants.GAMEHEIGHT - x:
                self.shoot = False
        self.animate(direction)

    def animate(self, direction):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 50:
            self.last_updated = now
            self.current_frame = (self.current_frame +
                                  1) % len(self.frames_right)
            if direction == 'left':
                self.current_image = self.frames_left[self.current_frame]
            elif direction == 'right':
                self.current_image = self.frames_right[self.current_frame]
            elif direction == 'up':
                self.current_image = self.frames_up[self.current_frame]
            elif direction == 'down':
                self.current_image = self.frames_down[self.current_frame]

    def load_frames(self, scale):
        my_spritesheet = Spritesheet('assets/fireball/fireball.png', scale)
        self.frames_right = [my_spritesheet.parse_sprite("FB001.png"), my_spritesheet.parse_sprite("FB002.png"),
                             my_spritesheet.parse_sprite(
                                 "FB003.png"), my_spritesheet.parse_sprite("FB004.png"),
                             my_spritesheet.parse_sprite("FB005.png")]
        self.frames_left = [pygame.transform.flip(
            frame, True, False) for frame in self.frames_right]
        self.frames_up = [pygame.transform.rotate(
            frame, 90) for frame in self.frames_right]
        self.frames_down = [pygame.transform.rotate(
            frame, 270) for frame in self.frames_right]


class HomingFireBall(EnemyFireBall):
    def __init__(self, scale, direction, target, smoothness=0.002):
        super().__init__(scale, direction)
        self.target = target
        self.smoothness = smoothness
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect.x = target.rect.x + random.randint(-300, 300)
        self.rect.y = 0
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)

    def update(self, x, direction, player):
        self.x_camera = x
        dx = self.target.rect.x - self.position.x
        dy = self.target.rect.y - self.position.y

        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            desired_velocity = pygame.math.Vector2(
                dx / distance * self.fireball_speed, dy / distance * self.fireball_speed)
            self.velocity = self.velocity.lerp(
                desired_velocity, self.smoothness)
            self.position.x += self.velocity.x
            self.position.y += self.velocity.y

            self.rect.x = int(self.position.x)
            self.rect.y = int(self.position.y)

        self.player_collision(player)
        self.animate(direction)


class Character(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, width=32, height=48, max_health=200, attack_range=50, attack_cooldown=1000):
        pygame.sprite.Sprite.__init__(self)
        self.position, self.velocity = pygame.math.Vector2(x, y), pygame.math.Vector2(0, 0)
        self.gravity, self.friction = 0.35, -0.12
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.on_ground = False

        # Attributes
        self.health = max_health
        self.max_health = max_health
        self.state = 'idle'
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
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
        # Override this method in subclasses to implement AI behavior
        pass

    def attack(self, player):
        player.health -= 10
        self.position.x = player.position.x+1
        self.position.y = player.position.y
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
        self.position.y += self.velocity.y * dt + \
            (self.acceleration.y * .2) * (dt * dt)
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

        health_bar_filled = int(
            (self.health / self.max_health) * health_bar_width)

        health_bar_bg = pygame.Rect(
            health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        health_bar_fill = pygame.Rect(
            health_bar_x, health_bar_y, health_bar_filled, health_bar_height)

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


class Creep(Character):
    def __init__(self, x=0, y=0):
        self.load_frames()
        self.current_image = self.running_frames_right[0]
        self.current_frame = 0
        self.last_updated = 0
        # self.image.fill((255, 0, 255))
        self.rect = self.attacking_frames_left[0].get_rect()
        super().__init__(x, y, width=32, height=48, max_health=200,
                         attack_range=50, attack_cooldown=1000)
        # self.load_frames()
        self.state = 'moving left'

    def handle_ai(self, dt, player,tiles,csv):
        # distance_to_player = self.position.x - player.position.x

        # # Chase the player if they are within 250 units
        # if -250 < distance_to_player < 250:
        #     if distance_to_player > 0:
        #         self.acceleration.x = -0.1
        #     elif distance_to_player < 0:
        #         self.acceleration.x = 0.1

        #     # Attack the player if they are within the attack range and the attack is not on cooldown
        #     if distance_to_player < self.attack_range and ((pygame.time.get_ticks() - self.last_attack) > self.attack_cooldown):
        #         self.attack(player)
        # else:
        #     # Randomly choose a direction to move if the player is not within range
        #     self.acceleration.x = random.choice([-0.01, 0, 0.01])
        distance_to_player = math.sqrt((self.position.x - player.position.x)**2 + (self.position.y - player.position.y)**2)

        # Chase the player if they are within 250 units
        if  distance_to_player < 100:
            if self.position.x - player.position.x > 0:
                self.state = 'moving left'
                self.acceleration.x = -0.1
            elif self.position.x - player.position.x < 0:
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

class ShootingMonster(Character):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, width=32, height=48, max_health=200,
                         attack_range=200, attack_cooldown=1000)
        self.fireball = EnemyFireBall(1, 'left')

    def handle_ai(self, dt, player):
        distance_to_player_x = self.position.x - player.position.x
        distance_to_player_y = self.position.y - player.position.y

        if abs(distance_to_player_x) < self.attack_range and pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
            self.attack(player)
            self.shoot_fireball(player)

    def attack(self, player):
        super().attack(player)
        self.last_attack = pygame.time.get_ticks()

    def shoot_fireball(self, player):
        if not self.fireball.shoot:
            self.fireball.rect.x = self.rect.x
            self.fireball.rect.y = self.rect.y
            self.fireball.shoot = True

            distance_to_player_x = self.position.x - player.position.x
            distance_to_player_y = self.position.y - player.position.y

            if abs(distance_to_player_x) > abs(distance_to_player_y):
                if distance_to_player_x > 0:
                    self.fireball.direction = 'left'
                else:
                    self.fireball.direction = 'right'
            else:
                if distance_to_player_y > 0:
                    self.fireball.direction = 'up'
                else:
                    self.fireball.direction = 'down'

    def update(self, dt, tiles, player):
        self.handle_ai(dt, player)
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)
        if self.fireball.shoot:
            self.fireball.update(self.fireball.x_camera,
                                 self.fireball.direction)

    def draw(self, display, x, y, tiles):
        super().draw_health_bar(display)
        display.blit(self.image, (self.rect.x + x, self.rect.y + y))
        if self.fireball.shoot:
            self.fireball.draw(display, x, y, tiles)


class Boss(Character):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, width=64, height=96, max_health=500,
                         attack_range=300, attack_cooldown=1000)
        self.load_frames()
        self.current_image = self.attacking_frames_right[0]
        self.current_frame = 0
        self.last_updated = 0
        # self.image.fill((255, 0, 255))
        self.rect = self.attacking_frames_left[0].get_rect()
        self.fireball = EnemyFireBall(1, 'down')
        self.homing_fireballs = []

    def handle_ai(self, dt, player):
        distance_to_player = self.position.x - player.position.x

        # Chase the player if they are within attack_range units
        if -self.attack_range < distance_to_player < self.attack_range:
            # if distance_to_player > 0:
            #     self.acceleration.x = -0.15
            # elif distance_to_player < 0:
            #     self.acceleration.x = 0.15

            # Attack the player if they are within the attack range and the attack is not on cooldown
            if abs(distance_to_player) < self.attack_range and pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                # self.attack(player)
                # self.summon_fireball(player)
                self.shoot_homing_fireball(player)
                if (random.randint(0, 1) < 0.02):
                    self.fire_rain(player)
        # else:
        #     # Randomly choose a direction to move if the player is not within range
        #     self.acceleration.y += random.choice([ 0, 3])

    def fire_rain(self, player):
        for _ in range(0, 3):
            homing_fireball = HomingFireBall(1, 'down', player)
            homing_fireball.shoot = True
            self.homing_fireballs.append(homing_fireball)

    def horizontal_movement(self, dt):
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(0.1)
        self.position.x += self.velocity.x * dt
        self.rect.x = self.position.x

    def summon_fireball(self, player):
        if not self.fireball.shoot:
            self.fireball.rect.x = player.rect.x
            self.fireball.rect.y = 0
            self.fireball.shoot = True
            self.fireball.direction = 'down'

    def shoot_homing_fireball(self, player):
        self.last_attack = pygame.time.get_ticks()

        homing_fireball = HomingFireBall(1, 'down', player)
        homing_fireball.shoot = True
        self.homing_fireballs.append(homing_fireball)

    def update(self, dt, tiles, player,csv):
        self.handle_ai(dt, player)
        self.animate()
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)
        self.vertical_movement(dt)
        self.check_collisions_y(tiles)
        if self.fireball.shoot:
            self.fireball.update(self.fireball.x_camera,
                                 self.fireball.direction)
        for homing_fireball in self.homing_fireballs:
            if homing_fireball.shoot:
                homing_fireball.update(
                    homing_fireball.x_camera, homing_fireball.direction, player)

    def draw(self, display, x, y, tiles, player):
        # self.draw_health_bar(display)
        display.blit(self.current_image, (self.rect.x + x, self.rect.y + y))
        if self.fireball.shoot:
            self.fireball.draw(display, x, y, tiles, player)
        for homing_fireball in self.homing_fireballs:
            if homing_fireball.shoot:
                homing_fireball.draw(display, x, y, tiles, player)
                
    def load_frames(self):
        my_spritesheet = Spritesheet('assets/boss/mage.png',1)
        self.attacking_frames_right = [my_spritesheet.parse_sprite("Attack (1).png"),my_spritesheet.parse_sprite("Attack (2).png"),
                                     my_spritesheet.parse_sprite("Attack (3).png"),my_spritesheet.parse_sprite("Attack (4).png"),
                                     my_spritesheet.parse_sprite("Attack (5).png"),my_spritesheet.parse_sprite("Attack (6).png"),
                                     my_spritesheet.parse_sprite("Attack (7).png"),my_spritesheet.parse_sprite("Attack (8).png")]
        self.attacking_frames_left = []
        for frame in self.attacking_frames_right:
            self.attacking_frames_left.append( pygame.transform.flip(frame,True, False) )
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 30:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.attacking_frames_right)
            self.current_image = self.attacking_frames_right[self.current_frame]

