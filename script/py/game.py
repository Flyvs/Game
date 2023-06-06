# imports
import pygame
import sys
import json
import os

from battle import Battle
from pause import Pause
from music import Music
from camera import Camera
from enemy import Enemy
from npc import NPC
from player import Player
from expandList import ExpandList
from crypting import Crypting
from gamepad import Inputs


class Game():
    # initializing
    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.font.init()

        # set to true when converting the script to an exe and to false when running in editor
        Game.export = False

        # getting paths
        Game.jsonPath = Game.path("script")
        Game.msgboxPath = Game.path("sprites", "msgboxes")
        Game.enemyPath = Game.path("sprites", "enemies")
        Game.mergePath = Game.path("temp")
        Game.npcPath = Game.path("sprites", "NPCs")
        Game.playerPath = Game.path("sprites", "player")
        Game.attackSpritePath = Game.path("sprites", "attack")
        Game.musicPath = Game.path("music")

        # encrypting the json
        try:
            Game.cryptingPath = Game.path("script")
            Crypting.rename(Game.cryptingPath,
                            "gamedata.rofl", "gamedata.json")
            Crypting.rename(Game.cryptingPath,
                            "playerdata.rofl", "playerdata.json")
            Crypting.decrypt(Game.cryptingPath, "gamedata.json", "gamekey.key")
            Crypting.decrypt(Game.cryptingPath,
                             "playerdata.json", "playerkey.key")
        except:
            pass

        # loading the jsons
        Game.gamedatafile = open(Game.jsonPath + "gamedata.json", "r")
        Game.gamedata = json.load(Game.gamedatafile)
        Game.gamedatafile.close()

        Game.playerdatafile = open(Game.jsonPath + "playerdata.json", "r")
        Game.playerdata = json.load(Game.playerdatafile)
        Game.playerdatafile.close()

        # getting the values from the json
        self.screenx = Game.gamedata["resolutionx"]
        self.screeny = Game.gamedata["resolutiony"]
        Game.fullscreen = Game.gamedata["fullscreen"]
        volume = Game.gamedata["volume"]

        # setting screen mode
        if Game.fullscreen == False:
            Game.screen = pygame.display.set_mode((self.screenx, self.screeny))
        elif Game.fullscreen == True:
            Game.screen = pygame.display.set_mode(
                (self.screenx, self.screeny), pygame.FULLSCREEN)

        # setting the game caption and icon
        pygame.display.set_caption("Game")
        icon = pygame.image.load(
            Game.path("sprites", "player") + "playerR.png")
        pygame.display.set_icon(icon)

        # initializing variables
        self.clock = pygame.time.Clock()
        Game.run = "mainmenu"
        Game.ground = "ground:0"

        Game.ticksToIgnoreTAB = 0
        Game.ticksToIgnoreSPACE = 0

        Game.playerHitTicks = 0
        Game.playerHitSeconds = 0
        Game.playerHitMinutes = 0
        Game.playerHitHours = 0

        Game.camera = Camera(Game, Player)
        Game.pause = Pause(Game, Player)
        Game.battle = Battle(Game, Player)

        Enemy.list = []
        enemy1 = Enemy(Game.camera, (100, 1768), 1, 32, 10, 9, 12, 7, 15, 1, True, "testenemy.png", Game, Player)
        enemy2 = Enemy(Game.camera, (300, 1768), 1, 32, 10, 9, 12, 7, 15, 2, True, "testenemy2.png", Game, Player)
        enemy3 = Enemy(Game.camera, (1000, 1768), 1, 32, 10, 9, 12, 7, 15, 3, True, "testenemy3.png", Game, Player)
        ExpandList.expand(Enemy.list, enemy1, enemy2, enemy3)

        NPC((500, 1768), Game.npcPath, Game.camera)
        Game.playerLoaded = False

        self.music = Music(Game.musicPath, Game)
        self.music.play(1, volume)

        self.main()

    def main(self):
        # main process of the game
        while True:
            while Game.run == "mainmenu":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_mainmenu()

            while Game.run == "game":
                Game.gamepadInputs = Inputs.scan()[0]
                # always gives the player 3 seconds invincibility after running away from an enemy
                timer = Game.tracktime(
                    Game.playerHitTicks, Game.playerHitSeconds, Game.playerHitMinutes, Game.playerHitHours)
                Game.playerHitTicks = timer["ticks"]
                Game.playerHitSeconds = timer["seconds"]
                if timer["seconds"] % 3 == 0 and Player.hit is False:
                    Game.playerHitTicks = 0
                    Game.playerHitSeconds = 0
                    Player.hit = True
                else:
                    # ========================================================================
                    Enemy.findPlayer()
                self.run_game()

            while Game.run == "pause":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_pause()

            while Game.run == "options":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_options()

            while Game.run == "resolution":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_resolution()

            while Game.run == "volume":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_volume()

            while Game.run == "battle":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_battle()

            while Game.run == "items":
                Game.gamepadInputs = Inputs.scan()[0]
                self.run_items()

    def exit():
        # encrypting the json and exiting afterwards
        Crypting.encrypt(Game.cryptingPath, "gamedata.json", "gamekey.key")
        Crypting.encrypt(Game.cryptingPath, "playerdata.json", "playerkey.key")
        Crypting.rename(Game.cryptingPath, "gamedata.json", "gamedata.rofl")
        Crypting.rename(Game.cryptingPath,
                        "playerdata.json", "playerdata.rofl")
        pygame.quit()
        sys.exit()

    def getName(input: str):
        file = input
        chars = []

        for char in file:
            chars.append(char)
        chars.reverse()
        fileChars = []

        for char in chars:
            if not char == "\\":
                fileChars.append(char)
            else:
                fileChars.reverse()
                break

        file = "".join(fileChars)
        return file

    # creates a path to files
    def path(newPath: str = None, newPath2: str = None):
        absolutePath = os.path.abspath(os.path.join(
            os.path.abspath(__file__), os.pardir))
        fileDirectory = os.path.dirname(absolutePath)
        parentDirectory = os.path.dirname(fileDirectory)
        if Game.export:
            dirName = os.path.abspath(__file__)
            dirName = os.path.dirname(os.path.dirname(dirName))
            parentDirectory = os.path.join(
                parentDirectory, Game.getName(dirName))
            parentDirectory = os.path.join(
                parentDirectory, Game.getName(__file__[:-3]))
        if newPath != None:
            parentDirectory = os.path.join(parentDirectory, newPath)
        if newPath2 != None:
            parentDirectory = os.path.join(parentDirectory, newPath2)
        parentDirectory = parentDirectory + "\\"
        return parentDirectory

    # teleports the player and sets the ground
    def teleport(self, groundA: str, groundB: str, hitboxX: int, hitboxY: int, hitboxWidth: int, hitboxHeigth: int):
        if (Player.player_teleport_collision(self, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)) and (Game.ground == groundA):
            Camera.ground(Camera.grounds[1])
            Player.rect.center = (640, 360)
            Game.ground = groundB
        elif (Player.player_teleport_collision(self, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)) and (Game.ground == groundB):
            Camera.ground(Camera.grounds[0])
            Player.rect.center = (640, 360)
            Game.ground = groundA

    # tracks the time
    def tracktime(ticks: int, seconds: int, minutes: int, hours: int):
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
                Game.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.run = "pause"
        try:
            if Game.gamepadInputs[16] == 1:
                Game.run = "pause"
        except:
            # If no gamepad is connected an exception ("NoneType" object is not subscriptable) occurs
            pass

        self.screen.fill('#71ddee')
        Game.camera.update()
        Game.camera.custom_draw(Game.player, Enemy.list)
        pygame.display.update()
        self.clock.tick(60)

    # sets details for battlescreen
    def run_battle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#91ddee')
        Battle.battleScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for itemscreen
    def run_items(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#91ddee')
        Game.battle.itemScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for pausescreen
    def run_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#71ddee')
        Game.pause.pauseScreen()
        pygame.display.update()
        self.clock.tick(20)

    # sets details for optionscreen
    def run_options(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#71ddee')
        Game.pause.option_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for resolutionscreen
    def run_resolution(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#71ddee')
        Game.pause.resolution_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for mainmenu
    def run_mainmenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#71ddee')
        Game.pause.mainmenu_screen()

        pygame.display.update()
        self.clock.tick(20)

    # sets details for volumescreen
    def run_volume(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.exit()

        self.screen.fill('#71ddee')
        Game.pause.volume_screen()

        pygame.display.update()
        self.clock.tick(20)


# starting the game
if __name__ == "__main__":
    Game()
