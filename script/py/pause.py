import pygame
import json
import os

from camera import Camera
from music import Music

class Pause():
    # initializing
    def __init__(self, game, player):
        super().__init__()
        Pause.game = game
        Pause.player = player
        Pause.sprites = Pause.game.path("sprites")

        self.mainmenu_options = []
        self.pause_options = []
        self.option_options = []
        self.resolution_options = []
        self.volume_options = []

        # getting the sprites
        for file in os.listdir(Pause.sprites + "mainmenu"):
            mainmenu = pygame.image.load(Pause.sprites + "\\mainmenu\\" + file)
            self.mainmenu_options.append(mainmenu)

        for file in os.listdir(Pause.sprites + "pause"):
            pause = pygame.image.load(Pause.sprites + "pause\\" + file)
            self.pause_options.append(pause)

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
        self.options_slider = Pause.game.gamedata["volume"]
        self.options_accessed = ""

        self.resx = Pause.game.gamedata["resolutionx"]
        self.resy = Pause.game.gamedata["resolutiony"]

    # save options
    def save_options(self, newResX: int, newResY: int, fullscreen: bool):
        Pause.game.gamedata["resolutionx"] = newResX
        Pause.game.gamedata["resolutiony"] = newResY
        Pause.game.gamedata["fullscreen"] = fullscreen

        Pause.game.gamedatafile = open(Pause.game.jsonPath + "gamedata.json", "w")
        json.dump(Pause.game.gamedata, Pause.game.gamedatafile)
        Pause.game.gamedatafile.close()

    # save position
    def save_pos(self):
        try:
            Pause.game.playerdata["playerx"] = Pause.player.rect.center[0]
            Pause.game.playerdata["playery"] = Pause.player.rect.center[1]

            Pause.game.playerdatafile = open(Pause.game.jsonPath + "playerdata.json", "w")
            json.dump(Pause.game.playerdata, Pause.game.playerdatafile)
            Pause.game.playerdatafile.close()
        except:
            pass

    # load position
    def load_pos(self):
        if Pause.game.playerLoaded == False:
            Pause.game.player = Pause.player((Pause.game.playerdata["playerx"], Pause.game.playerdata["playery"]), Pause.game, Pause.game.jsonPath, Pause.game.playerPath, Pause.game.attackSpritePath, Pause.game.camera)
            Pause.game.playerLoaded = True

        Pause.game.playerdatafile = open(Pause.game.jsonPath + "playerdata.json", "w")
        json.dump(Pause.game.playerdata, Pause.game.playerdatafile)
        Pause.game.playerdatafile.close()

    # save volume
    def save_volume(self):
        Pause.game.gamedata["volume"] = self.options_slider
        volume = Pause.game.gamedata["volume"]
        Music.volume(self, volume)

        Pause.game.gamedatafile = open(Pause.game.jsonPath + "gamedata.json", "w")
        json.dump(Pause.game.gamedata, Pause.game.gamedatafile)
        Pause.game.gamedatafile.close()

    # volume screen
    def volume_screen(self):
        keys = pygame.key.get_pressed()
        display_volume = pygame.font.SysFont("Aerial", 100)
        volume_surface = display_volume.render(str(self.options_slider), False, (0, 0, 0))

        if keys[pygame.K_a] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[23] == 1):
            if self.options_slider != 0:
                self.options_slider -= 1
        elif keys[pygame.K_d] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[24] == 1):
            if self.options_slider != 20:
                self.options_slider += 1
        elif (keys[pygame.K_SPACE] and Pause.game.ticksToIgnoreSPACE == 0) or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[10] == 1 and Pause.game.ticksToIgnoreSPACE == 0):
            Pause.game.ticksToIgnoreSPACE = 5
            Pause.game.run = "options"
        
        if Pause.game.ticksToIgnoreSPACE > 0:
            Pause.game.ticksToIgnoreSPACE -= 1

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

        if keys[pygame.K_w] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[21] == 1):
            if self.options_mainmenu != 1:
                self.options_mainmenu -= 1
        elif keys[pygame.K_s] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[22] == 1):
            if self.options_mainmenu != 4:
                self.options_mainmenu += 1
        elif (keys[pygame.K_SPACE] and Pause.game.ticksToIgnoreSPACE == 0) or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[10] == 1 and Pause.game.ticksToIgnoreSPACE == 0):
            Pause.game.ticksToIgnoreSPACE = 5
            if self.options_mainmenu == 1:
                if Pause.game.playerLoaded == False:
                    Pause.game.player = Pause.player((640, 1780), Pause.game, Pause.game.jsonPath, Pause.game.playerPath, Pause.game.attackSpritePath, Pause.game.camera)
                    Pause.game.playerLoaded = True
                Pause.player.rect.center = (640, 1780)
                Pause.game.run = "game"
                pygame.time.wait(100)
            elif self.options_mainmenu == 2:
                Pause.load_pos(self)
                Pause.game.run = "game"
            elif self.options_mainmenu == 3:
                Pause.game.run = "options"
                pygame.time.wait(100)
            elif self.options_mainmenu == 4:
                self.save_options(self.resx, self.resy, Pause.game.fullscreen)
                self.save_pos()
                Pause.game.exit()
        
        if Pause.game.ticksToIgnoreSPACE > 0:
            Pause.game.ticksToIgnoreSPACE -= 1

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

        if keys[pygame.K_w] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[21] == 1):
            if self.options_pause_menu != 1:
                self.options_pause_menu -= 1
        elif keys[pygame.K_s] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[22] == 1):
            if self.options_pause_menu != 5:
                self.options_pause_menu += 1
        elif (keys[pygame.K_SPACE] and Pause.game.ticksToIgnoreSPACE == 0) or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[10] == 1 and Pause.game.ticksToIgnoreSPACE == 0):
            Pause.game.ticksToIgnoreSPACE = 5
            if self.options_pause_menu == 1:
                Pause.game.run = "options"
            elif self.options_pause_menu == 2:
                self.save_options(self.resx, self.resy, Pause.game.fullscreen)
                self.save_pos()
            elif self.options_pause_menu == 3:
                Pause.game.run = "game"
            elif self.options_pause_menu == 4:
                self.save_options(self.resx, self.resy, Pause.game.fullscreen)
                self.save_pos()
                Pause.game.run = "mainmenu"
            elif self.options_pause_menu == 5:
                self.save_options(self.resx, self.resy, Pause.game.fullscreen)
                self.save_pos()
                Pause.game.exit()
        
        if Pause.game.ticksToIgnoreSPACE > 0:
            Pause.game.ticksToIgnoreSPACE -= 1

        if self.options_pause_menu == 1:
            Camera.displaySurface.blit(self.pause_options[2], (0, 0))
        elif self.options_pause_menu == 2:
            Camera.displaySurface.blit(self.pause_options[4], (0, 0))
        elif self.options_pause_menu == 3:
            Camera.displaySurface.blit(self.pause_options[3], (0, 0))
        elif self.options_pause_menu == 4:
            Camera.displaySurface.blit(self.pause_options[1], (0, 0))
        elif self.options_pause_menu == 5:
            Camera.displaySurface.blit(self.pause_options[0], (0, 0))

    # option screen
    def option_screen(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[21] == 1):
            if self.options_option_menu != 1:
                self.options_option_menu -= 1
        elif keys[pygame.K_s] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[22] == 1):
            if self.options_option_menu != 3:
                self.options_option_menu += 1
        elif (keys[pygame.K_SPACE] and Pause.game.ticksToIgnoreSPACE == 0) or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[10] == 1 and Pause.game.ticksToIgnoreSPACE == 0):
            Pause.game.ticksToIgnoreSPACE = 5
            if self.options_option_menu == 1:
                Pause.game.run = "resolution"
                pygame.time.wait(100)
                pass
            elif self.options_option_menu == 2:
                Pause.game.run = "volume"
                pygame.time.wait(100)
            elif self.options_option_menu == 3:
                if self.options_accessed == "mainmenu":
                    Pause.game.run = "mainmenu"
                elif self.options_accessed == "pause":
                    Pause.game.run = "pause"
                pygame.time.wait(100)
        
        if Pause.game.ticksToIgnoreSPACE > 0:
            Pause.game.ticksToIgnoreSPACE -= 1

        if self.options_option_menu == 1:
            Camera.displaySurface.blit(self.option_options[1], (0, 0))
        elif self.options_option_menu == 2:
            Camera.displaySurface.blit(self.option_options[2], (0, 0))
        elif self.options_option_menu == 3:
            Camera.displaySurface.blit(self.option_options[0], (0, 0))

    # resolution screen
    def resolution_screen(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[21] == 1):
            if self.options_resolution != 1:
                self.options_resolution -= 1
        elif keys[pygame.K_s] or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[22] == 1):
            if self.options_resolution != 6:
                self.options_resolution += 1
        elif (keys[pygame.K_SPACE] and Pause.game.ticksToIgnoreSPACE == 0) or (Pause.game.gamepadInputs != None and Pause.game.gamepadInputs[10] == 1 and Pause.game.ticksToIgnoreSPACE == 0):
            Pause.game.ticksToIgnoreSPACE = 5
            if self.options_resolution == 1:
                self.resx = 1280
                self.resy = 720
                Pause.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 2:
                self.resx = 1920
                self.resy = 1080
                Pause.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 3:
                self.resx = 1920
                self.resy = 1080
                Pause.game.fullscreen = True
                self.screen = pygame.display.set_mode(
                    (self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 4:
                self.resx = 2560
                self.resy = 1080
                Pause.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 5:
                self.resx = 3440
                self.resy = 1440
                Pause.game.fullscreen = True
                self.screen = pygame.display.set_mode((self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 6:
                Pause.game.run = "options"
                self.save_options(self.resx, self.resy, Pause.game.fullscreen)
                pygame.time.wait(100)

        if Pause.game.ticksToIgnoreSPACE > 0:
            Pause.game.ticksToIgnoreSPACE -= 1

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
