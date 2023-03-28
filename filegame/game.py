import pygame
from .menu import *
from .spritesheet import Spritesheet
from .player1 import Player
from .player2 import *
from .constants import GameConstants
# from .spritesheet import Spritesheet
from .camera import Camera
from .tiles import *
clock = pygame.time.Clock() 
# delay_time = 300
pygame.mixer.init()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.set_volume(0.2)
class Game():
    def __init__(self):
        pygame.init()
        self.running,self.playing = True,False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False
        self.width,self.height = GameConstants.GAMEWIDTH, GameConstants.GAMEHEIGHT
        self.display = pygame.Surface((self.width,self.height))
        self.window = pygame.display.set_mode((self.width,self.height))
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK,self.WHITE = (0,0,0),(255,255,255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.fps = 60
        self.player1 = Player()
        self.player2 = Player2()
        self.player = self.player1
        self.camera = Camera(self.player)
        self.spritesheet = Spritesheet('assets/map/spritesheet.png',1)
        self.map = TileMap('assets/map/map.csv', self.spritesheet )
        self.monster = pygame.image.load('assets/zombie/png/male/Attack (1).png')
        self.monster= pygame.transform.scale(self.monster,(50,50))
        self.switch = 1
        self.delay =0
        # self.fireball = FireBall()
    def game_loop(self):
        # i=1 ####
        pygame.mixer.music.play(-1)
        dt = clock.tick(60) * .001 * self.fps
        while self.playing:
            # i=(i+1)%len(self.knight1)
            self.check_events()
            if self.START_KEY:
                self.playing = False
            # UPDATE SPRITE,CAMERA
            # self.delay+=3
            # if delay > delay_time:
            # print(self.switch)
            # print
            if self.player == self.player1 and self.switch ==2:
                self.player2.position.x = self.player1.position.x
                self.player2.position.y = self.player1.position.y
                self.player = self.player2
            if self.player == self.player2 and self.switch ==1:
                self.player1.position.x = self.player2.position.x
                self.player1.position.y = self.player2.position.y
                self.player = self.player1
            self.camera = Camera(self.player)
            self.player.update(dt,self.map.tiles,pygame.Rect(680+self.camera.x,530+self.camera.y,self.monster.get_width(),self.monster.get_height()))
            self.camera.scroll()
            ########## DISPLAY #######
            # self.display.fill(self.BLACK)
            # self.monster = pygame.image.load('assets/zombie/png/male/Attack (1).png')
            # self.monster= pygame.transform.scale(self.monster,(50,50))
            self.display = pygame.image.load('assets/map/Background.png')
            self.display= pygame.transform.scale(self.display,(1440,810))
            self.draw_text("PLAYING",20,self.width/2,self.height/2)
            self.window.blit(self.display,(int(self.camera.x),int(self.camera.y)))
            self.map.draw_map(self.window,(int(self.camera.x),int(self.camera.y)))
            self.window.blit(self.monster,(680+self.camera.x,530+self.camera.y))
            self.window.blit(self.player.current_image,(int(self.player.rect.x + self.camera.x),int(self.player.rect.y + self.camera.y)))
            if self.player == self.player2:
                if self.player.fireball.shoot:
                    self.player.fireball.draw(self.window,self.camera.x,self.camera.y,self.map.tiles)
            pygame.display.update()
            self.reset_keys() 
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False,False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    # self.player.JUMP = True
                if event.key == pygame.K_LEFT:
                    self.player.LEFT_KEY = True
                    self.player.FACING_LEFT = True
                if event.key == pygame.K_RIGHT:
                    self.player.RIGHT_KEY = True
                    self.player.FACING_LEFT = False
                if event.key == pygame.K_z :
                    self.player.ATK=True
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_s:
                    # print(self.switch)
                    if self.switch == 1:
                        self.switch =2
                    elif self.switch == 2:
                        self.switch = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.LEFT_KEY = False
                if event.key == pygame.K_RIGHT:
                    self.player.RIGHT_KEY = False
                if event.key == pygame.K_UP:
                    self.player.JUMP = False
                if event.key == pygame.K_z:
                    self.player.ATK=False
                if event.key == pygame.K_SPACE:
                    if self.player.is_jumping:
                        self.player.velocity.y *= .25
                        self.player.is_jumping = False
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False
    def draw_text(self,text,size,x,y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text,True,self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
