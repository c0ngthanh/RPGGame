import pygame
from .menu import *
from .spritesheet import Spritesheet
from .player1 import Player
from .player2 import *
from .constants import GameConstants
# from .spritesheet import Spritesheet
from .camera import Camera
from .tiles import *
from .enemy import Creep, Boss, ShootingMonster
from .item import Item, Coin, Shield, Booster, HealthPack
from .chest import Chest

clock = pygame.time.Clock()
# delay_time = 300
pygame.mixer.init()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.set_volume(0.2)
RED = (255,0,0)
class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.width, self.height = GameConstants.GAMEWIDTH, GameConstants.GAMEHEIGHT
        self.display = pygame.Surface((self.width, self.height))
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.fps = 45
        self.player1 = Player()
        self.player2 = Player2()
        self.player = self.player1
        #self.enemy = ShootingMonster(200, 500)
        # self.boss = Creep(200, 500)
        self.enemy = [Creep(200, 500),Creep(500, 500),Creep(600, 500),Creep(700, 500),Creep(800, 500),Creep(1700,500),Boss(3392,700)]
        # item
        self.chest = Chest(1000,600)
        self.coin = Coin(400, 500)
        self.items = self.chest.items
        self.dropItem = False
        self.camera = Camera(self.player)
        self.spritesheet = Spritesheet('assets/map/spritesheet.png', 1)
        self.map = TileMap('assets/map/map.csv', self.spritesheet)
        self.switch = 1
        self.delay =0
        self.BG = 1
        # self.fireball = FireBall()
    def renderText(self,text,size,x,y,color):
        font = pygame.font.Font('time new roman.ttf',size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.window.blit(text_surface,text_rect)
    def game_loop(self):
        # i=1 ####
        pygame.mixer.music.play(-1)
        dt = clock.tick(60) * .001 * self.fps
        while self.playing:
            if self.player.health <=0 :
                return
            # i=(i+1)%len(self.knight1)
            self.check_events()
            if self.START_KEY:
                self.playing = False
            # UPDATE SPRITE,CAMERA
            # self.delay+=3
            # if delay > delay_time:
            # print(self.switch)
            # print
            if self.player == self.player1 and self.switch == 2:
                self.player2.position.x = self.player1.position.x
                self.player2.position.y = self.player1.position.y
                self.player = self.player2
            if self.player == self.player2 and self.switch == 1:
                self.player1.position.x = self.player2.position.x
                self.player1.position.y = self.player2.position.y
                self.player = self.player1
            self.camera = Camera(self.player)
            self.player.update(dt,self.map.tiles,self.enemy)
            #self.enemy.update(dt, self.map.tiles, self.player)
            for i in range(len(self.enemy)):
                self.enemy[i].update(dt,self.map.tiles, self.player,self.map.csv)


            self.camera.scroll()
            ########## DISPLAY #######
            # self.display.fill(self.BLACK)
            # self.monster = pygame.image.load('assets/zombie/png/male/Attack (1).png')
            # self.monster= pygame.transform.scale(self.monster,(50,50))
            self.BG = pygame.image.load('assets/map/Background.png')
            self.BG= pygame.transform.scale(self.BG,(1440,810))
            # self.draw_text("PLAYING",20,self.width/2,self.height/2,RED)
            self.window.blit(self.BG,(int(self.camera.x),int(self.camera.y)))
            self.window.blit(self.BG,(int(self.camera.x)+1440,int(self.camera.y)))
            self.window.blit(self.BG,(int(self.camera.x)+2880,int(self.camera.y)))
            self.map.draw_map(self.window,(int(self.camera.x),int(self.camera.y)))
            # self.window.blit(self.monster,(680+self.camera.x,530+self.camera.y))
            self.window.blit(self.player.current_image,(int(self.player.rect.x + self.camera.x),int(self.player.rect.y + self.camera.y)))
            # print(self.chest.rect)
            self.chest.update(dt,self.map.tiles)
            if not self.chest.delete:
                self.window.blit(self.chest.current_image,(int(self.chest.rect.x + self.camera.x),int(self.chest.rect.y + self.camera.y)))
            if self.player == self.player2:
                if self.player.fireball.shoot:
                    self.player.fireball.draw(
                        self.window, self.camera.x, self.camera.y, self.map.tiles)
            # self.window.blit(self.enemy.image, (int(
            #     self.enemy.rect.x + self.camera.x), int(self.enemy.rect.y + self.camera.y)))
            # self.window.blit(self.coin.image, (int(self.coin.rect.x + self.camera.x), int(self.coin.rect.y + self.camera.y)))        
            # self.window.blit(self.boss.image, (int(
            #     self.boss.rect.x + self.camera.x), int(self.boss.rect.y + self.camera.y)))
            
            #Fireball shooting
            for i in range(len(self.enemy)):
                if type(self.enemy[i]) is Boss:
                    self.enemy[i].draw(self.window, self.camera.x, self.camera.y, self.map.tiles, self.player)
            # Update and draw item
            for i in range(len(self.enemy)):
                self.window.blit(self.enemy[i].current_image, (int(self.enemy[i].rect.x + self.camera.x), int(self.enemy[i].rect.y + self.camera.y)))
            if self.chest.is_open:
                self.dropItem = True
            for item in self.items:
                if not item.collected and self.dropItem:
                    item.update(self.player)
                    self.window.blit(item.image, (int(
                        item.rect.x + self.camera.x), int(item.rect.y + self.camera.y)))
            # Remove collected items from the list
            self.items = [item for item in self.items if not item.collected]
            pygame.draw.rect(self.window,self.player.get_color(),pygame.Rect(0,0,self.player.health*2,30))
            self.renderText('HP: ' +str(self.player.health) + "/100",20,0,0,self.WHITE)
            pygame.draw.rect(self.window,(128,128,0),pygame.Rect(0,30,self.player.EXP*20,30))
            self.renderText('Exp: ' +str(self.player.EXP) + "/10",20,0,30,self.WHITE)
            self.renderText('Level: ' +str(self.player.LEVEL),20,0,60,self.WHITE)
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
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
                    self.player.ATK = True
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_s:
                    # print(self.switch)
                    if self.switch == 1:
                        self.switch = 2
                    elif self.switch == 2:
                        self.switch = 1
                if event.key == pygame.K_x:
                    if pygame.Rect.colliderect(self.player.rect,self.chest.rect):
                        self.chest.is_open = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.LEFT_KEY = False
                if event.key == pygame.K_RIGHT:
                    self.player.RIGHT_KEY = False
                if event.key == pygame.K_UP:
                    self.player.JUMP = False
                if event.key == pygame.K_z:
                    self.player.ATK = False
                if event.key == pygame.K_SPACE:
                    if self.player.is_jumping:
                        self.player.velocity.y *= .25
                        self.player.is_jumping = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False,False,False,False
    def draw_text(self,text,size,x,y,color=(255,255,255)):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
