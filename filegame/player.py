import pygame
from .spritesheet import Spritesheet
from .constants import GameConstants
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT,self.ATK,self.JUMP = False, False, False,False,False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.midbottom = (240, 244)
        self.ground_y = 224
        self.current_frame = 0
        self.last_updated = 0
        self.velocityX = 0
        self.velocityY = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_right[0]
    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self):
        self.velocityX = 0
        self.velocityY = 0
        self.ATKSPD = 0
        if self.LEFT_KEY:
            self.velocityX += -10
        if self.RIGHT_KEY:
            self.velocityX += 10
        if self.JUMP:
            self.velocityY = -50
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY + 0.5*9.8
        # print(self.rect.x)
        # print(self.rect.w)
        if(self.rect.y>244):
            self.rect.y=244
        if(self.rect.x > GameConstants.BACKGROUNWIDTH - self.rect.w):
            self.rect.x = GameConstants.BACKGROUNWIDTH - self.rect.w
        if(self.rect.x < 0):
            self.rect.x =  0
        self.set_state()
        for i in range(10):
            self.animate()
    def set_state(self):
        self.state = 'idle'
        if self.velocityX > 0:
            self.state = 'moving right'
        elif self.velocityX < 0:
            self.state = 'moving left'
        elif self.ATK:
            self.state = 'attack'
        elif self.velocityY < 0:
            self.state = 'jumping'
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
            if now - self.last_updated > 1:
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
            self.jumping_frames_left.append( pygame.transform.flip(frame,True, False) )
        











