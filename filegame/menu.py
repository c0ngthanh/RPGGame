import pygame
# from .game import *
class Menu:
    def __init__(self, game):
            self.game = game
            self.mid_w,self.mid_h = game.width /2 , game.height /2 
            self.run_display = True
            self.cursor_rect = pygame.Rect(0,0,20,20)
            self.offset = -100
    def draw_cursor(self):
        self.game.draw_text("*",15,self.cursor_rect.x,self.cursor_rect.y)
    def blit_screen(self):
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.state = "Start"
        self.startx,self.starty = self.mid_w,self.mid_h + 30
        self.optionx,self.optiony = self.mid_w,self.mid_h + 50
        self.creditx,self.credity = self.mid_w,self.mid_h + 70
        self.cursor_rect.midtop=(self.startx+self.offset,self.starty)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.move_cursor()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu",20,self.mid_w,self.mid_h - 20)
            self.game.draw_text("Start",20,self.startx,self.starty)
            self.game.draw_text("Option",20,self.optionx,self.optiony)
            self.game.draw_text("Credit",20,self.creditx,self.credity)
            self.draw_cursor()
            self.blit_screen()
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionx + self.offset,self.optiony)
                self.state = "Option"
            elif self.state == "Option":
                self.cursor_rect.midtop = (self.creditx + self.offset,self.credity)
                self.state = "Credit"
            elif self.state == "Credit":
                self.cursor_rect.midtop = (self.startx + self.offset,self.starty)
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditx + self.offset,self.credity)
                self.state = "Credit"
            elif self.state == "Option":
                self.cursor_rect.midtop = (self.startx + self.offset,self.starty)
                self.state = "Start"
            elif self.state == "Credit":
                self.cursor_rect.midtop = (self.optionx + self.offset,self.optiony)
                self.state = "Option"
    def check_input(self):
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Option":
                self.game.curr_menu = self.game.options
            elif self.state == "Credit":
                self.game.curr_menu = self.game.credits
        self.run_display = False
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.state = 'Volume'
        self.volx,self.voly = self.mid_w, self.mid_h+20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Options", 20, self.game.width/2, self.game.height/2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.width / 2, self.game.height / 2 - 20)
            self.game.draw_text('Made by me', 15, self.game.width / 2, self.game.height / 2 + 10)
            self.blit_screen()