import pygame
import os
import random
import math
import pygame.mixer



class Item(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, scale_factor=1):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.scale_image(scale_factor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hover_timer = 0
        self.hover_range = 1
        self.collected = False

    def scale_image(self, scale_factor):
        width = int(self.image.get_width() * scale_factor)
        height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (width, height))
        

    def update(self):
        # Add update logic for the item, e.g., moving or animating
        self.hover()
        pass
    
    def check_collision(self, player):
        return self.rect.colliderect(player.rect)
    
    def respawn(self, x_range, y_range):
        self.rect.x = random.randint(x_range[0], x_range[1])
        self.rect.y = random.randint(y_range[0], y_range[1])
        
    def hover(self):
        self.hover_timer += 0.05
        hover_offset = (0.5  - math.sin(self.hover_timer)) * self.hover_range
        self.rect.y += hover_offset

class Coin(Item):
    def __init__(self, x, y, scale_factor = 0.2):
        super().__init__("./assets/images/coins.png", x, y)
        super().scale_image(scale_factor)
        self.angle = 0 # Initial rotate angle
        self.original_image = self.image # Save image for rotation
        self.flip_timer = 0  # Initialize the flip timer
        self.scale_factor = 1.0  # Initialize the scale factor
        self.growing = False  # Initialize the scaling direction
        self.pickup_sound = pygame.mixer.Sound("./assets/sounds/coin_pickup.mp3")
        
    def update(self, player):
        self.hover()
        self.rotate_horizontally_smooth()
        if self.check_collision(player):
            self.pickup_sound.play()
            print('touched')
            self.collected = True

    def rotate(self):
        self.angle = (self.angle + 1) % 360  # Increment the angle and keep it within 0-359 degrees
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to keep the same center
        
    def flip_horizontally(self):
        self.flip_timer += 1  # Increment the flip timer
        if self.flip_timer % 60 == 0:  # Flip the image every 10 frames
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.original_image, self.image = self.image, self.original_image  # Swap the images
            
    def rotate_horizontally_smooth(self):
        if self.scale_factor >= 1.0:
            self.growing = False
        elif self.scale_factor <= 0.5:
            self.growing = True

        self.scale_factor += 0.002 if self.growing else -0.002

        width = int(self.original_image.get_width() * self.scale_factor)
        height = self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to keep the same center
        

class Booster(Item):
    def __init__(self, x, y, scale_factor = 1):
        super().__init__("./assets/images/speed_potion.png", x, y)
        super().scale_image(scale_factor)
        self.pickup_sound = pygame.mixer.Sound("./assets/sounds/power_up.wav")

    def update(self, player):
        self.hover()
        if self.check_collision(player):
            self.pickup_sound.play()
            self.apply_effect(player)
            print('touched')
            self.collected = True

    def apply_effect(self, player):
        player.speed_booster = True
        player.speed_temp = 5
        player.speed_timer = pygame.time.get_ticks()
        
        
class Shield(Item):
    def __init__(self, x, y, scale_factor=0.6):
        super().__init__("./assets/images/Shield.png", x, y, scale_factor)
        self.pickup_sound = pygame.mixer.Sound("./assets/sounds/power_up.wav")

    def update(self, player):
        self.hover()
        if self.check_collision(player):
            self.pickup_sound.play()
            self.apply_effect(player)
            print('Shield picked up')
            self.collected = True

    def apply_effect(self, player):
        player.shield_active = True
        player.shield_timer = pygame.time.get_ticks()

class HealthPack(Item):
    def __init__(self, x, y, scale_factor=0.6):
        super().__init__("./assets/images/heatFull.png", x, y, scale_factor)
        self.pickup_sound = pygame.mixer.Sound("./assets/sounds/health_pack.wav")

    def update(self, player):
        self.hover()
        if self.check_collision(player):
            self.pickup_sound.play()
            self.apply_effect(player)
            print('Health pack picked up')
            self.collected = True

    def apply_effect(self, player):
        player.health += 25
        if player.health > player.max_health:
            player.health = player.max_health