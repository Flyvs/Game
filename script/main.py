# imports
import pygame
import sys
import json
import os

from camera import Camera
from pause import Pause
#from npc import NPC
from music import Music
from battle import Battle
from player import Player
from enemy import Enemy

from numba import cuda, jit
# @jit(target_backend='cuda') <-- this before calling a function makes use of the GPU


class Game():
    # initializing
    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.font.init()

        # getting paths for json; msgbox; enemy
        Game.jsonPath = Game.path("script") + "data.json"
        Game.msgboxPath = Game.path("sprites", "msgboxes")
        Game.enemyPath = Game.path("sprites", "enemies")

        # loading the json
        Game.fileR = open(Game.jsonPath, "r")
        Game.data = json.load(Game.fileR)
        Game.fileR.close()

        # getting the values from the json
        self.screenx = Game.data["resolutionx"]
        self.screeny = Game.data["resolutiony"]
        Game.fullscreen = Game.data["fullscreen"]
        volume = Game.data["volume"]

        # setting screen mode
        if Game.fullscreen == False:
            Game.screen = pygame.display.set_mode((self.screenx, self.screeny))
        elif Game.fullscreen == True:
            Game.screen = pygame.display.set_mode((self.screenx, self.screeny), pygame.FULLSCREEN)

        # setting the game caption and icon
        pygame.display.set_caption("test")
        icon = pygame.image.load(Game.path("sprites", "player") + "playerR.png")
        pygame.display.set_icon(icon)

        # initializing variables
        self.clock = pygame.time.Clock()
        Game.run = "mainmenu"
        Game.ground = "ground:0"
        Game.itemSpawned = False
        Game.itemRespawn = 5  # -------------------------------------------------------------------------------------------------------------------------
        Game.whichItem = 0
        Game.i = 0

        Game.ticksToIgnoreTAB = 0
        Game.ticksToIgnoreSPACE = 0

        Game.ticks = 0
        Game.seconds = 0
        Game.minutes = 0
        Game.hours = 0
        Game.playerHitTicks = 0
        Game.playerHitSeconds = 0
        Game.playerHitMinutes = 0
        Game.playerHitHours = 0

        Game.camera = Camera()
        Game.pause = Pause()
        Game.battle = Battle()

        Game.NPC1 = NPC((500, 10), Game.camera)
        Game.playerLoaded = False

        self.music = Music()
        self.music.play(2, volume)

        # main process of the game
        while True:
            while Game.run == "mainmenu":
                self.run_mainmenu()

            while Game.run == "game":
                # always gives the player 3 seconds invincibility after running away from an enemy
                timer = Game.tracktime(Game.playerHitTicks, Game.playerHitSeconds, Game.playerHitMinutes, Game.playerHitHours)
                Game.playerHitTicks = timer["ticks"]
                Game.playerHitSeconds = timer["seconds"]
                if timer["seconds"] % 3 == 0 and Player.hit == False:
                    Game.playerHitTicks = 0
                    Game.playerHitSeconds = 0
                    Player.hit = True
                else:
                    try:
                        Enemy.findPlayer()  # ========================================================================================================================================================
                    except:
                        pass
                self.run_game()

            while Game.run == "pause":
                self.run_pause()

            while Game.run == "options":
                self.run_options()

            while Game.run == "resolution":
                self.run_resolution()

            while Game.run == "volume":
                self.run_volume()

            while Game.run == "battle":
                self.run_battle()

            while Game.run == "items":
                self.run_items()

    # creates a path to files
    def path(newPath: str = None, newPath2: str = None):
        absolutePath = os.path.abspath(__file__)
        fileDirectory = os.path.dirname(absolutePath)
        parentDirectory = os.path.dirname(fileDirectory)
        # parentDirectory = os.path.join(parentDirectory, "game") remove comment when converted to an exe and comment when run in editor------------------------------------------------------------------
        if newPath != None:
            parentDirectory = os.path.join(parentDirectory, newPath)
        if newPath2 != None:
            parentDirectory = os.path.join(parentDirectory, newPath2)
        parentDirectory = parentDirectory + "\\"
        return parentDirectory

    # teleports the player and sets the ground
    def teleport(self, hitboxX: int, hitboxY: int, hitboxWidth: int, hitboxHeigth: int):
        if (Player.player_teleport_collision(self, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)) and (Game.ground != "ground:1"):
            Camera.ground(Camera.grounds[1])
            Player.rect.center = (640, 360)
            Game.ground = "ground:1"
        elif (Player.player_teleport_collision(self, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)) and (Game.ground != "ground:0"):
            Camera.ground(Camera.grounds[0])
            Player.rect.center = (640, 360)
            Game.ground = "ground:0"

    # tracks the time
    def tracktime(ticks, seconds, minutes, hours):
        if ticks % 60 == 0:
            seconds += 1
            ticks = 0
            if seconds % 60 == 0:
                minutes += 1
                seconds = 0
                if minutes % 60 == 0:
                    hours += 1
                    minutes = 0
        ticks += 1
        return {"ticks": ticks, "seconds": seconds, "minutes": minutes, "hours": hours}

    # sets details for main game
    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.run = "pause"

        self.screen.fill('#71ddee')
        Game.camera.update()
        Game.camera.custom_draw(Game.player)
        pygame.display.update()
        self.clock.tick(60)

    # sets details for battlescreen
    def run_battle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#91ddee')
        Battle.battleScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for itemscreen
    def run_items(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#91ddee')
        Game.battle.itemScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for pausescreen
    def run_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#71ddee')
        Game.pause.pauseScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for optionscreen
    def run_options(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#71ddee')
        Game.pause.option_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for resolutionscreen
    def run_resolution(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#71ddee')
        Game.pause.resolution_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for mainmenu
    def run_mainmenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#71ddee')
        Game.pause.mainmenu_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for volumescreen
    def run_volume(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill('#71ddee')
        Game.pause.volume_screen()

        pygame.display.update()
        self.clock.tick(20)