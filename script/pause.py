import pygame
import os
import json
import sys

from music import Music
from camera import Camera
from player import Player
from game import Game

class Pause():
    # initializing
    def __init__(self):
        super().__init__()
        Pause.sprites = Game.path("sprites")

        self.mainmenu_options = []
        Game.pause_options = []
        self.option_options = []
        self.resolution_options = []
        self.volume_options = []

        # getting the sprites
        for file in os.listdir(Pause.sprites + "mainmenu"):
            mainmenu = pygame.image.load(Pause.sprites + "\\mainmenu\\" + file)
            self.mainmenu_options.append(mainmenu)

        for file in os.listdir(Pause.sprites + "pause"):
            pause = pygame.image.load(Pause.sprites + "pause\\" + file)
            Game.pause_options.append(pause)

        for file in os.listdir(Pause.sprites + "options"):
            options = pygame.image.load(Pause.sprites + "options\\" + file)
            self.option_options.append(options)

        for file in os.listdir(Pause.sprites + "resolution"):
            resolution = pygame.image.load(Pause.sprites + "resolution\\" + file)
            self.resolution_options.append(resolution)

        for file in os.listdir(Pause.sprites + "volumeslider"):
            volume = pygame.image.load(Pause.sprites + "volumeslider\\" + file)
            self.volume_options.append(volume)

        self.options_mainmenu = 1
        self.options_pause_menu = 1
        self.options_option_menu = 1
        self.options_resolution = 1
        self.options_slider = Game.data["volume"]
        self.options_accessed = ""

        self.resx = Game.data["resolutionx"]
        self.resy = Game.data["resolutiony"]

    # save options
    def save_options(self, newResX: int, newResY: int, fullscreen: bool):
        Game.data["resolutionx"] = newResX
        Game.data["resolutiony"] = newResY
        Game.data["fullscreen"] = fullscreen

        Game.fileW = open(Game.jsonPath, "w")
        json.dump(Game.data, Game.fileW)
        Game.fileW.close()

    # save position
    def save_pos(self):
        Game.data["playerx"] = Player.rect.center[0]
        Game.data["playery"] = Player.rect.center[1]

        Game.fileW = open(Game.jsonPath, "w")
        json.dump(Game.data, Game.fileW)
        Game.fileW.close()

    # load position
    def load_pos(self):
        if Game.playerLoaded == False:
            Game.player = Player((Game.data["playerx"], Game.data["playery"]), Game.camera)
            Game.playerLoaded = True

        Game.fileW = open(Game.jsonPath, "w")
        json.dump(Game.data, Game.fileW)
        Game.fileW.close()

    # save volume
    def save_volume(self):
        Game.data["volume"] = self.options_slider
        volume = Game.data["volume"]
        Music.volume(self, volume)

        Game.fileW = open(Game.jsonPath, "w")
        json.dump(Game.data, Game.fileW)
        Game.fileW.close()

    # volume screen
    def volume_screen(self):
        keys = pygame.key.get_pressed()
        display_volume = pygame.font.SysFont("Aerial", 100)
        volume_surface = display_volume.render(str(self.options_slider), False, (0, 0, 0))

        if keys[pygame.K_a]:
            if self.options_slider != 0:
                self.options_slider -= 1
        elif keys[pygame.K_d]:
            if self.options_slider != 20:
                self.options_slider += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            Game.run = "options"
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if self.options_slider == 0:
            Camera.displaySurface.blit(self.volume_options[0], (0, 0))
        elif self.options_slider == 1:
            Camera.displaySurface.blit(self.volume_options[1], (0, 0))
        elif self.options_slider == 2:
            Camera.displaySurface.blit(self.volume_options[12], (0, 0))
        elif self.options_slider == 3:
            Camera.displaySurface.blit(self.volume_options[14], (0, 0))
        elif self.options_slider == 4:
            Camera.displaySurface.blit(self.volume_options[15], (0, 0))
        elif self.options_slider == 5:
            Camera.displaySurface.blit(self.volume_options[16], (0, 0))
        elif self.options_slider == 6:
            Camera.displaySurface.blit(self.volume_options[17], (0, 0))
        elif self.options_slider == 7:
            Camera.displaySurface.blit(self.volume_options[18], (0, 0))
        elif self.options_slider == 8:
            Camera.displaySurface.blit(self.volume_options[19], (0, 0))
        elif self.options_slider == 9:
            Camera.displaySurface.blit(self.volume_options[20], (0, 0))
        elif self.options_slider == 10:
            Camera.displaySurface.blit(self.volume_options[2], (0, 0))
        elif self.options_slider == 11:
            Camera.displaySurface.blit(self.volume_options[3], (0, 0))
        elif self.options_slider == 12:
            Camera.displaySurface.blit(self.volume_options[4], (0, 0))
        elif self.options_slider == 13:
            Camera.displaySurface.blit(self.volume_options[5], (0, 0))
        elif self.options_slider == 14:
            Camera.displaySurface.blit(self.volume_options[6], (0, 0))
        elif self.options_slider == 15:
            Camera.displaySurface.blit(self.volume_options[7], (0, 0))
        elif self.options_slider == 16:
            Camera.displaySurface.blit(self.volume_options[8], (0, 0))
        elif self.options_slider == 17:
            Camera.displaySurface.blit(self.volume_options[9], (0, 0))
        elif self.options_slider == 18:
            Camera.displaySurface.blit(self.volume_options[10], (0, 0))
        elif self.options_slider == 19:
            Camera.displaySurface.blit(self.volume_options[11], (0, 0))
        elif self.options_slider == 20:
            Camera.displaySurface.blit(self.volume_options[13], (0, 0))

        Camera.displaySurface.blit(pygame.image.load(Pause.sprites + "sliderBackYES.png"), (0, 0))
        Camera.displaySurface.blit(volume_surface, (600, 265))
        self.save_volume()

    # main menu screen
    def mainmenu_screen(self):
        keys = pygame.key.get_pressed()
        self.options_accessed = "mainmenu"

        if keys[pygame.K_w]:
            if self.options_mainmenu != 1:
                self.options_mainmenu -= 1
        elif keys[pygame.K_s]:
            if self.options_mainmenu != 4:
                self.options_mainmenu += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            if self.options_mainmenu == 1:
                if Game.playerLoaded == False:
                    Game.player = Player((640, 360), Game.camera)
                    Game.playerLoaded = True
                Player.rect.center = (640, 360)
                Game.run = "game"
                pygame.time.wait(100)
            elif self.options_mainmenu == 2:
                Pause.load_pos(self)
                Game.run = "game"
            elif self.options_mainmenu == 3:
                Game.run = "options"
                pygame.time.wait(100)
            elif self.options_mainmenu == 4:
                self.save_options(self.resx, self.resy, Game.fullscreen)
                try:
                    self.save_pos()
                except:
                    sys.exit()
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if self.options_mainmenu == 1:
            Camera.displaySurface.blit(self.mainmenu_options[3], (0, 0))
        elif self.options_mainmenu == 2:
            Camera.displaySurface.blit(self.mainmenu_options[1], (0, 0))
        elif self.options_mainmenu == 3:
            Camera.displaySurface.blit(self.mainmenu_options[2], (0, 0))
        elif self.options_mainmenu == 4:
            Camera.displaySurface.blit(self.mainmenu_options[0], (0, 0))

    # pause screen
    def pauseScreen(self):
        keys = pygame.key.get_pressed()
        self.options_accessed = "pause"

        if keys[pygame.K_w]:
            if self.options_pause_menu != 1:
                self.options_pause_menu -= 1
        elif keys[pygame.K_s]:
            if self.options_pause_menu != 5:
                self.options_pause_menu += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            if self.options_pause_menu == 1:
                Game.run = "options"
            elif self.options_pause_menu == 2:
                self.save_options(self.resx, self.resy, Game.fullscreen)
                self.save_pos()
            elif self.options_pause_menu == 3:
                Game.run = "game"
            elif self.options_pause_menu == 4:
                self.save_options(self.resx, self.resy, Game.fullscreen)
                self.save_pos()
                Game.run = "mainmenu"
            elif self.options_pause_menu == 5:
                self.save_options(self.resx, self.resy, Game.fullscreen)
                self.save_pos()
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if self.options_pause_menu == 1:
            Camera.displaySurface.blit(Game.pause_options[2], (0, 0))
        elif self.options_pause_menu == 2:
            Camera.displaySurface.blit(Game.pause_options[4], (0, 0))
        elif self.options_pause_menu == 3:
            Camera.displaySurface.blit(Game.pause_options[3], (0, 0))
        elif self.options_pause_menu == 4:
            Camera.displaySurface.blit(Game.pause_options[1], (0, 0))
        elif self.options_pause_menu == 5:
            Camera.displaySurface.blit(Game.pause_options[0], (0, 0))

    # option screen
    def option_screen(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.options_option_menu != 1:
                self.options_option_menu -= 1
        elif keys[pygame.K_s]:
            if self.options_option_menu != 3:
                self.options_option_menu += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            if self.options_option_menu == 1:
                Game.run = "resolution"
                pygame.time.wait(100)
                pass
            elif self.options_option_menu == 2:
                Game.run = "volume"
                pygame.time.wait(100)
            elif self.options_option_menu == 3:
                if self.options_accessed == "mainmenu":
                    Game.run = "mainmenu"
                elif self.options_accessed == "pause":
                    Game.run = "pause"
                pygame.time.wait(100)
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if self.options_option_menu == 1:
            Camera.displaySurface.blit(self.option_options[1], (0, 0))
        elif self.options_option_menu == 2:
            Camera.displaySurface.blit(self.option_options[2], (0, 0))
        elif self.options_option_menu == 3:
            Camera.displaySurface.blit(self.option_options[0], (0, 0))

    # resolution screen
    def resolution_screen(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.options_resolution != 1:
                self.options_resolution -= 1
        elif keys[pygame.K_s]:
            if self.options_resolution != 6:
                self.options_resolution += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            if self.options_resolution == 1:
                self.resx = 1280
                self.resy = 720
                Game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 2:
                self.resx = 1920
                self.resy = 1080
                Game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 3:
                self.resx = 1920
                self.resy = 1080
                Game.fullscreen = True
                self.screen = pygame.display.set_mode(
                    (self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 4:
                self.resx = 2560
                self.resy = 1080
                Game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 5:
                self.resx = 3440
                self.resy = 1440
                Game.fullscreen = True
                self.screen = pygame.display.set_mode((self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 6:
                Game.run = "options"
                self.save_options(self.resx, self.resy, Game.fullscreen)
                pygame.time.wait(100)

        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if self.options_resolution == 1:
            Camera.displaySurface.blit(self.resolution_options[0], (0, 0))
        elif self.options_resolution == 2:
            Camera.displaySurface.blit(self.resolution_options[1], (0, 0))
        elif self.options_resolution == 3:
            Camera.displaySurface.blit(self.resolution_options[2], (0, 0))
        elif self.options_resolution == 4:
            Camera.displaySurface.blit(self.resolution_options[3], (0, 0))
        elif self.options_resolution == 5:
            Camera.displaySurface.blit(self.resolution_options[4], (0, 0))
        elif self.options_resolution == 6:
            Camera.displaySurface.blit(self.resolution_options[5], (0, 0))

        Camera.half_w = Camera.displaySurface.get_size()[0] // 2
        Camera.half_h = Camera.displaySurface.get_size()[1] // 2
        Camera.internal_offset.x = Camera.internal_surf_size[0] // 2 - Camera.half_w
        Camera.internal_offset.y = Camera.internal_surf_size[1] // 2 - Camera.half_h