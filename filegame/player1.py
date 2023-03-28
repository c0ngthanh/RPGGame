import pygame
from .spritesheet import Spritesheet
from .constants import GameConstants
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Stats 
        self.health = 100
        self.DEF = 3
        self.DMG = 5
        self.SPD = 1
        self.EXP = 0
        self.LEVEL = 0
        # Animation
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT,self.ATK,self.JUMP = False, False, False,False,False
        self.on_ground = False
        self.gravity = 0.35
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.gravity, self.friction = .35, -.12
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.current_frame = 0
        self.last_updated = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
        self.action_cooldown =1
    # Draw on surface 
    def draw(self, display):
        display.blit(self.current_image, self.rect)
    # Update state, animation, position of player 
    def update(self, dt, tiles,surface):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
        self.checkATK(surface)
    #Draw ATK state
    def checkATK(self,surface):
        if self.ATK:
            self.state = 'attack'
            self.animate()
            self.action_cooldown +=3
            action_wait_time = 100
            if self.action_cooldown > action_wait_time:
                if pygame.Rect.colliderect(self.rect,surface):
                    self.health-=1
                    print(self.health)
                    self.action_cooldown =0
    # Di chuyen theo phuong ngang, co ma sat, animation
    def horizontal_movement(self,dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .2
            self.state = 'moving left'
            self.animate()
        elif self.RIGHT_KEY:
            self.acceleration.x += .2
            self.state = 'moving right'
            self.animate()
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        if(self.position.x > GameConstants.BACKGROUNWIDTH - self.rect.w):
            self.position.x = GameConstants.BACKGROUNWIDTH - self.rect.w
        if(self.position.x < 0):
            self.position.x =  0
        self.rect.x = self.position.x
        if not self.RIGHT_KEY or not self.LEFT_KEY:
            self.state = 'idle'
            self.animate()
    # Di chuyen theo phuong doc 
    def vertical_movement(self,dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y
    # limit_velocity
    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0
    # Jump 
    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            # self.state = 'jumping'
            # self.animate()
            self.velocity.y -= 10
            self.on_ground = False
    # Check if tiles meet player
    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits
    #Check x
    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x
    #Check y
    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
###########################################################################
    # def set_state(self):
    #     self.state = 'idle'
    #     if self.velocityX > 0:
    #         self.state = 'moving right'
    #     elif self.velocityX < 0:
    #         self.state = 'moving left'
    #     elif self.ATK:
    #         self.state = 'attack'
    #     elif self.velocityY < 0:
    #         self.state = 'jumping'
    # Load Frame - state
    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'idle':
            if now - self.last_updated > 50:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        elif self.state == 'moving right' or self.state == 'moving left':
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
                if self.state == 'attack' and self.FACING_LEFT:
                    self.current_image = self.attacking_frames_left[self.current_frame]
                elif self.state == 'attack' and not self.FACING_LEFT:
                    self.current_image = self.attacking_frames_right[self.current_frame]
        # else:
        #     if now - self.last_updated > 10:
        #         print(self.current_frame)
        #         self.last_updated = now
        #         self.current_frame = (self.current_frame + 1) % len(self.jumping_frames_left)
        #         if self.state == 'jumping' and self.FACING_LEFT:
        #             self.current_image = self.jumping_frames_left[self.current_frame]
        #         elif self.state == 'jumping' and not self.FACING_LEFT:
        #             self.current_image = self.jumping_frames_right[self.current_frame]
    #load frame png
    def load_frames(self):
        my_spritesheet = Spritesheet('assets/knight/knight.png',10)
        self.idle_frames_right = [my_spritesheet.parse_sprite("Idle__000.png"),my_spritesheet.parse_sprite("Idle__001.png"),
                                 my_spritesheet.parse_sprite("Idle__002.png"),my_spritesheet.parse_sprite("Idle__003.png"),
                                 my_spritesheet.parse_sprite("Idle__004.png"),my_spritesheet.parse_sprite("Idle__005.png"),
                                 my_spritesheet.parse_sprite("Idle__006.png"),my_spritesheet.parse_sprite("Idle__007.png"),
                                 my_spritesheet.parse_sprite("Idle__008.png"),my_spritesheet.parse_sprite("Idle__009.png")]
        self.attacking_frames_right = [my_spritesheet.parse_sprite("Attack__000.png"),my_spritesheet.parse_sprite("Attack__001.png"),
                                     my_spritesheet.parse_sprite("Attack__002.png"),my_spritesheet.parse_sprite("Attack__003.png"),
                                     my_spritesheet.parse_sprite("Attack__004.png"),my_spritesheet.parse_sprite("Attack__005.png"),
                                     my_spritesheet.parse_sprite("Attack__006.png"),my_spritesheet.parse_sprite("Attack__007.png"),
                                     my_spritesheet.parse_sprite("Attack__008.png"),my_spritesheet.parse_sprite("Attack__009.png")]
        self.running_frames_right = [my_spritesheet.parse_sprite("Run__000.png"),my_spritesheet.parse_sprite("Run__001.png"),
                                     my_spritesheet.parse_sprite("Run__002.png"),my_spritesheet.parse_sprite("Run__003.png"),
                                     my_spritesheet.parse_sprite("Run__004.png"),my_spritesheet.parse_sprite("Run__005.png"),
                                     my_spritesheet.parse_sprite("Run__006.png"),my_spritesheet.parse_sprite("Run__007.png"),
                                     my_spritesheet.parse_sprite("Run__008.png"),my_spritesheet.parse_sprite("Run__009.png")]
        self.jumping_frames_right = [my_spritesheet.parse_sprite("Jump__000.png"),my_spritesheet.parse_sprite("Jump__001.png"),
                                      my_spritesheet.parse_sprite("Jump__002.png"),my_spritesheet.parse_sprite("Jump__003.png"),
                                      my_spritesheet.parse_sprite("Jump__004.png"),my_spritesheet.parse_sprite("Jump__005.png"),
                                      my_spritesheet.parse_sprite("Jump__006.png"),my_spritesheet.parse_sprite("Jump__007.png"),
                                      my_spritesheet.parse_sprite("Jump__008.png"),my_spritesheet.parse_sprite("Jump__009.png"),]
        self.idle_frames_left = []
        for frame in self.idle_frames_right:
            self.idle_frames_left.append( pygame.transform.flip(frame,True, False) )
        self.running_frames_left = []
        for frame in self.running_frames_right:
            self.running_frames_left.append(pygame.transform.flip(frame, True, False))
        self.attacking_frames_left = []
        for frame in self.attacking_frames_right:
            self.attacking_frames_left.append( pygame.transform.flip(frame,True, False) )
        self.jumping_frames_left = []
        for frame in self.jumping_frames_right:
            self.jumping_frames_left.append( pygame.transform.flip(frame,True, False))

        











