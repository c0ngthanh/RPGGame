import pygame
from .menu import *
from .spritesheet import Spritesheet
from .player1 import Player
from .constants import GameConstants
# from .spritesheet import Spritesheet
from .camera import Camera
from .tiles import *
clock = pygame.time.Clock() 
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
        self.player = Player()
        self.camera = Camera(self.player)
        self.spritesheet = Spritesheet('assets/map/spritesheet.png',1)
        self.map = TileMap('assets/map/map.csv', self.spritesheet )
    def game_loop(self):
        # i=1 ####
        dt = clock.tick(60) * .001 * self.fps
        while self.playing:
            # i=(i+1)%len(self.knight1)
            self.check_events()
            if self.START_KEY:
                self.playing = False
            # UPDATE SPRITE,CAMERA
            self.player.update(dt,self.map.tiles)
            self.camera.scroll()
            ########## DISPLAY #######
            # self.display.fill(self.BLACK)
            self.display = pygame.image.load('assets/map/Background.png')
            self.display= pygame.transform.scale(self.display,(1440,810))
            self.draw_text("PLAYING",20,self.width/2,self.height/2)
            self.window.blit(self.display,(int(self.camera.x),int(self.camera.y)))
            self.map.draw_map(self.window,(int(self.camera.x),int(self.camera.y)))
            self.window.blit(self.player.current_image,(int(self.player.rect.x + self.camera.x),int(self.player.rect.y + self.camera.y)))
            # clock.tick(self.fps)
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
                if event.key == pygame.K_z:
                    self.player.ATK=True
                if event.key == pygame.K_SPACE:
                    self.player.jump()
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
