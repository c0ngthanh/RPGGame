from .player1 import Player
from .spritesheet import Spritesheet
from .constants import GameConstants
import pygame
pygame.mixer.init()
sound = pygame.mixer.Sound('assets/sounds/hit.mp3')
pygame.mixer.Sound.set_volume(sound,0.2)
class Player2(Player):
    def __init__(self):
        super().__init__()
        self.fireball = FireBall(1)
        # self.bigfireball = FireBall(0.5)
        self.fireball_FACING_LEFT = True
    def checkATK(self,surface):
        if self.ATK:
            self.state = 'attack'
            self.animate()
            if not self.fireball.shoot:
                self.fireball.rect.x = self.rect.x
                self.fireball.rect.y = self.rect.y
                self.fireball.shoot =True
                self.fireball.FACING_LEFT = self.FACING_LEFT
            # self.fireball.rect = self.rect
            
            #     print(1)
        # print(self.ATK)
        # print(self.FACING_LEFT)
        if pygame.Rect.colliderect(self.fireball.rect,surface):
            self.fireball.shoot = False
            self.fireball.rect.x = 0
            self.fireball.rect.y = 0
            self.health-=self.DMG
            self.levelup()
            sound.play()
            print(self.health)
        if self.fireball.shoot:
            self.fireball.update(self.fireball.x_camera,self.fireball.FACING_LEFT)
        # print(1)
    def load_frames(self):
        my_spritesheet = Spritesheet('assets/mage/mage.png',10)
        self.idle_frames_right = [my_spritesheet.parse_sprite("Idle__000.png"),my_spritesheet.parse_sprite("Idle__001.png"),
                                 my_spritesheet.parse_sprite("Idle__002.png"),my_spritesheet.parse_sprite("Idle__003.png"),
                                 my_spritesheet.parse_sprite("Idle__004.png"),my_spritesheet.parse_sprite("Idle__005.png"),
                                 my_spritesheet.parse_sprite("Idle__006.png"),my_spritesheet.parse_sprite("Idle__007.png"),
                                 my_spritesheet.parse_sprite("Idle__008.png"),my_spritesheet.parse_sprite("Idle__009.png")]
        self.attacking_frames_right = [my_spritesheet.parse_sprite("Throw__000.png"),my_spritesheet.parse_sprite("Throw__001.png"),
                                     my_spritesheet.parse_sprite("Throw__002.png"),my_spritesheet.parse_sprite("Throw__003.png"),
                                     my_spritesheet.parse_sprite("Throw__004.png"),my_spritesheet.parse_sprite("Throw__005.png"),
                                     my_spritesheet.parse_sprite("Throw__006.png"),my_spritesheet.parse_sprite("Throw__007.png"),
                                     my_spritesheet.parse_sprite("Throw__008.png"),my_spritesheet.parse_sprite("Throw__009.png")]
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
class FireBall():
    def __init__(self,scale):
        self.load_frames(scale)
        self.x_camera = 0
        self.rect = self.frames_right[0].get_rect()
        self.current_frame = 0
        self.last_updated = 0
        self.current_image = self.frames_right[0]
        self.shoot = False
        self.FACING_LEFT = True
    def checkcollision(self,tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.shoot = False
                return
    def draw(self, display,x,y,tiles):
        self.update(x,self.FACING_LEFT)
        self.checkcollision(tiles)
        display.blit(self.current_image, (self.rect.x+x,self.rect.y+y))
    def update(self,x,FACING_LEFT):
        self.x_camera = x
        # print(x)
        # self.rect.x -=1
        # if self.rect.x <0:
        #     # print(GameConstants.GAMEWIDTH-x)
        #     self.shoot = False
        if not FACING_LEFT:
            self.rect.x +=2
        # self.rect.x +=1
            if self.rect.x > GameConstants.GAMEWIDTH-x:
                self.shoot = False
        if FACING_LEFT:
            self.rect.x -=2
            # print(-x)
            if self.rect.x < -x:
                self.shoot = False
        self.animate(FACING_LEFT)
    def animate(self,FACING_LEFT):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 50:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.frames_right)
            if FACING_LEFT:
                self.current_image = self.frames_left[self.current_frame]
            elif not FACING_LEFT:
                self.current_image = self.frames_right[self.current_frame]
    def load_frames(self,scale):
        my_spritesheet = Spritesheet('assets/fireball/fireball.png',scale)
        self.frames_right =[my_spritesheet.parse_sprite("FB001.png"),my_spritesheet.parse_sprite("FB002.png"),
                            my_spritesheet.parse_sprite("FB003.png"),my_spritesheet.parse_sprite("FB004.png"),
                            my_spritesheet.parse_sprite("FB005.png")]
        self.frames_left = []
        for frame in self.frames_right:
            self.frames_left.append( pygame.transform.flip(frame,True, False))