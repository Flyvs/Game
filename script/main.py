# imports
import pygame
import sys
import json
import os
import random

from expandList import ExpandList
from pygame_merge import Merge
from crypting import Crypting
from gamepad import Inputs


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
        Game.mergePath = Game.path("temp")

        # encrypting the json
        Game.cryptingPath = Game.path("script")
        try:
            Crypting.decrypt(Game.cryptingPath, "data.json")
        except:
            pass

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
        pygame.display.set_caption("Game")
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

        Enemy.list = []
        #enemy1 = Enemy(Game.camera, (100, 100), 1, 32, 10, 9, 12, 7, 15, False, "testenemy.png")
        #enemy2 = Enemy(Game.camera, (700, 700), 1, 32, 10, 9, 12, 7, 15, False, "testenemy2.png")
        #enemy3 = Enemy(Game.camera, (1000, 500), 1, 32, 10, 9, 12, 7, 15, False, "testenemy3.png")
        #ExpandList.expand(Enemy.list, enemy1, enemy2, enemy3)

        self.music = Music()
        self.music.play(2, volume)

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
                timer = Game.tracktime(Game.playerHitTicks, Game.playerHitSeconds, Game.playerHitMinutes, Game.playerHitHours)
                Game.playerHitTicks = timer["ticks"]
                Game.playerHitSeconds = timer["seconds"]
                if timer["seconds"] % 3 == 0 and Player.hit == False:
                    Game.playerHitTicks = 0
                    Game.playerHitSeconds = 0
                    Player.hit = True
                else:
                    Enemy.findPlayer()  # ========================================================================
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
        Crypting.encrypt(Game.cryptingPath, "data.json")
        pygame.quit()
        sys.exit()


    def getFileName():
        file = __file__[:-3]
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
        absolutePath = os.path.abspath(__file__)
        fileDirectory = os.path.dirname(absolutePath)
        parentDirectory = os.path.dirname(fileDirectory)
        # parentDirectory = os.path.join(parentDirectory, Game.getFileName()) # remove comment when converted to an exe and comment when run in editor------------------------------------------------------------------
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
            pass

        self.screen.fill('#71ddee')
        Game.camera.update()
        Game.camera.custom_draw(Game.player)
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


class NPC(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        NPC.hitted = False
        NPC.path = Game.path("sprites", "NPCs")

        NPC.allItems = []
        NPC.image = pygame.image.load(NPC.path + NPC.spawn("testNPC")).convert_alpha()
        NPC.rect = NPC.image.get_rect(topleft=pos)

    # spawn the npc
    def spawn(item: str):
        for file in os.listdir(NPC.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # check if npc is hit
    def hit():
        collision_x = Player.rect[0] + 64 >= NPC.rect[0] and NPC.rect[0] + 64 >= Player.rect[0]
        collision_y = Player.rect[1] + 64 >= NPC.rect[1] and NPC.rect[1] + 64 >= Player.rect[1]
        return collision_y and collision_x


class MsgBox(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, text: str, font: str, fontSize: int, rgb: tuple, msgbox: str, group):
        super().__init__(group)

        font_ = pygame.font.SysFont(font, fontSize)
        box = pygame.image.load(Game.msgboxPath + msgbox)
        text_ = font_.render(text, True, rgb)
        self.image = Merge.surfaces(Game.mergePath, box, text_)
        self.rect = self.image.get_rect(topleft=pos)

    # NPC Msgbox
    def NPC(text: str, font: str, fontSize: int, rgb: tuple):
        MsgBox((NPC.rect[0] - 224, NPC.rect[1] - 192), text, font, fontSize, rgb, "test.png", Game.camera)

    # Cutszene Msgbox
    def Cutszene():
        pass


class HUD(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, pos, text: str, font: str, fontSize: int, rgb: tuple):
        super().__init__(group)

        font_ = pygame.font.SysFont(font, fontSize)
        HUD.image = font_.render(text, True, rgb)
        HUD.rect = HUD.image.get_rect(center=pos)


    def updateHUD(text: str, font: str, fontSize: int, rgb: tuple):
        Player.HUD_w = Player.rect.center[0] + 480
        Player.HUD_h = Player.rect.center[1] - 330
        pos = (Player.HUD_w, Player.HUD_h)

        font_ = pygame.font.SysFont(font, fontSize)
        HUD.image = font_.render(text, True, rgb)
        HUD.rect = HUD.image.get_rect(center=pos)



class Player(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        Player.LVL = Game.data["LVL"]
        Player.XP = Game.data["XP"]
        Player.HP = Game.data["HP"]
        Player.PHYATK = Game.data["PHYATK"]
        Player.MAGATK = Game.data["MAGATK"]
        Player.PHYDEF = Game.data["PHYDEF"]
        Player.MAGDEF = Game.data["MAGDEF"]
        Player.SPEED = Game.data["SPEED"]
        Player.STAMINA = Game.data["STAMINA"]

        Player.path = Game.path("sprites", "player")
        Player.right = "playerR.png"
        Player.left = "playerL.png"
        Player.rightB = "playerRblack.png"
        Player.leftB = "playerLblack.png"
        Player.facingLeft = False
        Player.facingRight = True
        Player.hit = True

        Player.color = "w" # w: white; b: black

        Player.image = pygame.image.load(Player.path + Player.right).convert_alpha()
        Player.rect = Player.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.standard = 10
        self.speed = self.standard
        
        Player.attack = Attack(Game.camera, "PHY", 55)

        Player.HUD_w = Player.rect.center[0] + 480
        Player.HUD_h = Player.rect.center[1] - 330
        Player.HUD = HUD(Game.camera, (Player.HUD_w, Player.HUD_h), f"Stamina: {Player.STAMINA}", None, 60, (255, 0, 0))
        
   # drains the players stamina
    def drain(self):
        timer = Game.tracktime(Game.playerHitTicks, Game.playerHitSeconds, Game.playerHitMinutes, Game.playerHitHours)
        if Player.color == "b" and Player.STAMINA > 0:
            Game.playerHitTicks = timer["ticks"]
            Game.playerHitSeconds = timer["seconds"]

            if timer["seconds"] % 2 == 0:
                Player.STAMINA -= 1
                Game.playerHitTicks = 0
                Game.playerHitSeconds = 0
        if Player.STAMINA == 0:
            Player.color = "w"
            self.playerImage()
        if Player.color == "w" and Player.STAMINA < Game.data["STAMINA"]:
            if timer["seconds"] % 2 == 0:
                Player.STAMINA += 1
                Game.playerHitTicks = 0
                Game.playerHitSeconds = 0
        if Player.color == "b":
            self.speed = self.standard * 1.5
        else:
            self.speed = self.standard
        

    # set controls for gamepad movement
    def gamepad(self):
        try:
            if Game.gamepadInputs[4] > 0:
                if self.col_bottom == False:
                    self.direction.y = Game.gamepadInputs[4]
                else:
                    self.direction.y = 0
            elif Game.gamepadInputs[4] < 0:
                if self.col_top == False:
                    self.direction.y = Game.gamepadInputs[4]
                else:
                    self.direction.y = 0

            if Game.gamepadInputs[3] > 0:
                if self.col_right == False:
                    Player.facingRight = True
                    Player.facingLeft = False
                    self.direction.x = Game.gamepadInputs[3]
                else:
                    self.direction.x = 0
            elif Game.gamepadInputs[3] < 0:
                if self.col_left == False:
                    Player.facingRight = False
                    Player.facingLeft = True
                    self.direction.x = Game.gamepadInputs[3]
                else:
                    self.direction.x = 0
        except:
            pass

    # set the keys for movement
    def keyboard(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_w]:
            if self.col_top == False:
                self.direction.y = -1
            else:
                self.direction.y = 0
        elif self.keys[pygame.K_s]:
            if self.col_bottom == False:
                self.direction.y = 1
            else:
                self.direction.y = 0
        else:
            self.direction.y = 0

        if self.keys[pygame.K_d]:
            Player.facingRight = True
            Player.facingLeft = False
            if self.col_right == False:
                self.direction.x = 1
            else:
                self.direction.x = 0
        elif self.keys[pygame.K_a]:
            Player.facingRight = False
            Player.facingLeft = True
            if self.col_left == False:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0

    
    def playerImage(self):
        if Player.facingLeft == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.left).convert_alpha()
            elif Player.color == "b" and Player.STAMINA > 0:
                Player.image = pygame.image.load(Player.path + Player.leftB).convert_alpha()
        elif Player.facingRight == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.right).convert_alpha()
            elif Player.color == "b" and Player.STAMINA > 0:
                Player.image = pygame.image.load(Player.path + Player.rightB).convert_alpha()

        if (self.keys[pygame.K_TAB] and Game.ticksToIgnoreTAB == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[13] == 1 and Game.ticksToIgnoreTAB == 0):
            Game.ticksToIgnoreTAB = 30
            if Player.color == "w":
                Player.color = "b"
            elif Player.color == "b":
                Player.color = "w"

        if Game.ticksToIgnoreTAB > 0:
            Game.ticksToIgnoreTAB -= 1

    # updating details
    def update(self):
        if self.screen_collision_left():
            self.col_left = True
        else:
            self.col_left = False
        if self.screen_collision_right():
            self.col_right = True
        else:
            self.col_right = False
        if self.screen_collision_top():
            self.col_top = True
        else:
            self.col_top = False
        if self.screen_collision_bottom():
            self.col_bottom = True
        else:
            self.col_bottom = False

        if NPC.hit() and NPC.hitted == False:
            NPC.hitted = True
            MsgBox.NPC("This is some test text", None, 60, (66, 135, 245))

        self.keyboard()
        self.gamepad()
        self.playerImage()
        self.drain()

        Player.rect.center += self.direction * self.speed
        Attack.input(self)
        HUD.updateHUD(f"Stamina: {Player.STAMINA - 1}", None, 60, (255, 0, 0))
        Enemy.attackPlayer(self)
        Game.teleport(self, "ground:0", "ground:1", 1948, 900, 52, 200)

    # collision with 2 objects
    def aabb_collision(self, a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
        self.collision_x = a_x + a_width >= b_x and b_x + b_width >= a_x
        self.collision_y = a_y + a_height >= b_y and b_y + b_height >= a_y
        return self.collision_y and self.collision_x

    # left screen collision
    def screen_collision_left(self):
        return Player.rect.center[0] <= 0

    # right screen collision
    def screen_collision_right(self):
        return Player.rect.center[0] >= Camera.basic_width

    # top screen collision
    def screen_collision_top(self):
        return Player.rect.center[1] <= 0

    # bottom screen collision
    def screen_collision_bottom(self):
        return Player.rect.center[1] >= Camera.basic_height

    # player enemy collision
    def player_enemy_collision(self):
        try:
            enemyToCheck = Enemy.list.pop(0)
            Enemy.list.append(enemyToCheck)
            return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, enemyToCheck.rect.center[0], enemyToCheck.rect.center[1], 64, 64)
        except:
            pass

    # player teleport collision
    def player_teleport_collision(self, hitboxX: int, hitboxY: int, hitboxWidth: int, hitboxHeigth: int):
        return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)


class Camera(pygame.sprite.Group):
    # initializing
    def __init__(self):
        super().__init__()
        Camera.displaySurface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        Camera.half_w = Camera.displaySurface.get_size()[0] // 2
        Camera.half_h = Camera.displaySurface.get_size()[1] // 2

        # ground
        Camera.grounds = []
        groundsPath = Game.path("sprites", "grounds")
        for file in os.listdir(groundsPath):
            ground = groundsPath + file
            Camera.grounds.append(ground)

        Camera.ground(Camera.grounds[0])
        Game.path()

        # zoom
        Camera.internal_surf_size = (2500, 2500)
        Camera.internal_surf = pygame.Surface(Camera.internal_surf_size, pygame.SRCALPHA)
        Camera.internal_rect = Camera.internal_surf.get_rect(center=(Camera.half_w, Camera.half_h))
        Camera.internal_surface_size_vector = pygame.math.Vector2(Camera.internal_surf_size)
        Camera.internal_offset = pygame.math.Vector2()
        Camera.internal_offset.x = Camera.internal_surf_size[0] // 2 - Camera.half_w
        Camera.internal_offset.y = Camera.internal_surf_size[1] // 2 - Camera.half_h

    # set ground
    def ground(whichGround: str):
        Camera.ground_surf = pygame.image.load(whichGround).convert_alpha()
        Camera.ground_rect = Camera.ground_surf.get_rect(topleft=(0, 0))
        Camera.basic_height = Camera.ground_surf.get_height()
        Camera.basic_width = Camera.ground_surf.get_width()

    # set camera
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - Camera.half_w
        self.offset.y = target.rect.centery - Camera.half_h

    # drawing
    def custom_draw(self, player):
        self.center_target_camera(player)
        Camera.internal_surf.fill('#71ddee')

        # ground
        ground_offset = Camera.ground_rect.topleft - self.offset + Camera.internal_offset
        Camera.internal_surf.blit(Camera.ground_surf, ground_offset)

        i = 0
        # Sorted List for drawing objects in order
        Camera.spriteList = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
        spriteListLen = len(Camera.spriteList)
        while spriteListLen > i:
            spriteListLen = len(Camera.spriteList)
            obj = str(type(Camera.spriteList[i - 1])).partition(".")[2].split("'")[0]
            if Attack.space == False and obj == "Attack":
                del Camera.spriteList[i - 1]
            if str(type(Camera.spriteList[1])).partition(".")[2].split("'")[0] == "Attack":
                del Camera.spriteList[1]
            if NPC.hit() == False and obj == "MsgBox":
                del Camera.spriteList[1]
            if str(type(Camera.spriteList[0])).partition(".")[2].split("'")[0] == "MsgBox":
                del Camera.spriteList[0]
            i += 1
        #print(Camera.spriteList)

        for sprite in Camera.spriteList:
            offset_pos = sprite.rect.topleft - self.offset + Camera.internal_offset
            Camera.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(Camera.internal_surf, Camera.internal_surface_size_vector)
        scaled_rect = scaled_surf.get_rect(center=(Camera.half_w, Camera.half_h))
        Camera.displaySurface.blit(scaled_surf, scaled_rect)

"""
class Item(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        Item.hitted = False
        Item.path = Game.path("sprites", "items")

        Item.allItems = []
        if Game.itemSpawned == False:
            Item.image = pygame.image.load(Item.path + Item.randomSpawn()).convert_alpha()
            Item.rect = Item.image.get_rect(topleft=pos)
            Game.itemSpawned = True

    # spawning a specific item
    def spawn(item: str):
        for file in os.listdir(Item.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # spawning a random item
    def randomSpawn():
        for file in os.listdir(Item.path):
            Item.allItems.append(file)
        if Game.itemSpawned == False:
            Game.whichItem = random.randint(0, len(Item.allItems) - 1)
            Game.itemSpawned = True
        return str(Item.allItems[Game.whichItem])

    # check if item is hit
    def hit():
        collision_x = Player.rect[0] + 64 >= Item.rect[0] and Item.rect[0] + 64 >= Player.rect[0]
        collision_y = Player.rect[1] + 64 >= Item.rect[1] and Item.rect[1] + 64 >= Player.rect[1]
        return collision_y and collision_x
"""

class Music():
    # initializing
    def __init__(self):
        super().__init__()

        Music.path = Game.path("music")

    # play
    def play(self, song: int, volume: float):
        song = song - 1
        pygame.mixer.init()
        self.songs = []

        for file in os.listdir(Music.path):
            self.songs.append(file)

        try:
            pygame.mixer.music.load(Music.path + self.songs[song])
            pygame.mixer.music.play(-1, 0, 0)
        except:
            pass

        if Game.data["volume"] > 20:
            Game.data["volume"] = 20
            volume = Game.data["volume"]
        elif Game.data["volume"] < 0:
            Game.data["volume"] = 0
            volume = Game.data["volume"]

        # read json data
        Game.fileW = open(Game.jsonPath, "w")
        json.dump(Game.data, Game.fileW)
        Game.fileW.close()

        self.volume(volume)

    # set volume
    def volume(self, volume: float):
        volume *= 1.5
        volume /= 50
        pygame.mixer.music.set_volume(volume)


class Pause():
    # initializing
    def __init__(self):
        super().__init__()
        Pause.sprites = Game.path("sprites")

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
        try:
            Game.data["playerx"] = Player.rect.center[0]
            Game.data["playery"] = Player.rect.center[1]

            Game.fileW = open(Game.jsonPath, "w")
            json.dump(Game.data, Game.fileW)
            Game.fileW.close()
        except:
            pass

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

        if keys[pygame.K_a] or (Game.gamepadInputs != None and Game.gamepadInputs[23] == 1):
            if self.options_slider != 0:
                self.options_slider -= 1
        elif keys[pygame.K_d] or (Game.gamepadInputs != None and Game.gamepadInputs[24] == 1):
            if self.options_slider != 20:
                self.options_slider += 1
        elif (keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[10] == 1 and Game.ticksToIgnoreSPACE == 0):
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

        if keys[pygame.K_w] or (Game.gamepadInputs != None and Game.gamepadInputs[21] == 1):
            if self.options_mainmenu != 1:
                self.options_mainmenu -= 1
        elif keys[pygame.K_s] or (Game.gamepadInputs != None and Game.gamepadInputs[22] == 1):
            if self.options_mainmenu != 4:
                self.options_mainmenu += 1
        elif (keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[10] == 1 and Game.ticksToIgnoreSPACE == 0):
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
                self.save_pos()
                Game.exit()
        
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

        if keys[pygame.K_w] or (Game.gamepadInputs != None and Game.gamepadInputs[21] == 1):
            if self.options_pause_menu != 1:
                self.options_pause_menu -= 1
        elif keys[pygame.K_s] or (Game.gamepadInputs != None and Game.gamepadInputs[22] == 1):
            if self.options_pause_menu != 5:
                self.options_pause_menu += 1
        elif (keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[10] == 1 and Game.ticksToIgnoreSPACE == 0):
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
                Game.exit()
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

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

        if keys[pygame.K_w] or (Game.gamepadInputs != None and Game.gamepadInputs[21] == 1):
            if self.options_option_menu != 1:
                self.options_option_menu -= 1
        elif keys[pygame.K_s] or (Game.gamepadInputs != None and Game.gamepadInputs[22] == 1):
            if self.options_option_menu != 3:
                self.options_option_menu += 1
        elif (keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[10] == 1 and Game.ticksToIgnoreSPACE == 0):
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

        if keys[pygame.K_w] or (Game.gamepadInputs != None and Game.gamepadInputs[21] == 1):
            if self.options_resolution != 1:
                self.options_resolution -= 1
        elif keys[pygame.K_s] or (Game.gamepadInputs != None and Game.gamepadInputs[22] == 1):
            if self.options_resolution != 6:
                self.options_resolution += 1
        elif (keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0) or (Game.gamepadInputs != None and Game.gamepadInputs[10] == 1 and Game.ticksToIgnoreSPACE == 0):
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


class Attack(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, CLASS: str, DMG: int):
        super().__init__(group)

        Attack.CLASS = CLASS
        Attack.DMG = DMG

        Attack.spritePath = Game.path("sprites", "attack")
        Attack.right = "attackRight.png"
        Attack.left = "attackLeft.png"
        Attack.firingLeft = False
        Attack.firingRight = False
        Attack.space = False
        Attack.xRight = Player.rect.center[0] + 48
        Attack.yRight = Player.rect.center[1] + 14
        Attack.xLeft = Player.rect.center[0] - 48
        Attack.yLeft = Player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
        Attack.rect = Attack.image.get_rect(center=Attack.posRight)

    # positioning the attack and set the attack key
    def input(self):
        self.keys = pygame.key.get_pressed()
        Attack.xRight = Player.rect.center[0] + 48
        Attack.yRight = Player.rect.center[1] + 14
        Attack.xLeft = Player.rect.center[0] - 48
        Attack.yLeft = Player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        if self.keys[pygame.K_SPACE] or (Game.gamepadInputs != None and Game.gamepadInputs[11] == 1):
            Attack.space = True
            if Player.facingLeft == True:
                Attack.image = pygame.image.load(Attack.spritePath + Attack.left).convert_alpha()
                Attack.rect = Attack.image.get_rect(center=Attack.posLeft)
            elif Player.facingRight == True:
                Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
                Attack.rect = Attack.image.get_rect(center=Attack.posRight)
        else:
            Attack.space = False


class Enemy(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, POS: tuple, LVL: int, HP: int, PHYATK: int, MAGATK: int, PHYDEF: int, MAGDEF: int, SPEED: int, SPAWNED: bool, SPRITE: str):
        super().__init__(group)

        self.POS = POS
        self.LVL = LVL
        self.HP = HP
        self.PHYATK = PHYATK
        self.MAGATK = MAGATK
        self.PHYDEF = PHYDEF
        self.MAGDEF = MAGDEF
        self.SPEED = SPEED
        self.SPAWNED = SPAWNED
        self.SPRITE = SPRITE

        self.image = pygame.image.load(Game.enemyPath + self.SPRITE).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.POS)

    # track position of player
    def findPlayer():
        for enemy in Enemy.list:
            direction = pygame.math.Vector2()
            speed = 1

            if Player.rect.center[0] > enemy.rect.center[0]:
                direction.x = speed
            elif Player.rect.center[0] < enemy.rect.center[0]:
                direction.x = -speed

            if Player.rect.center[1] > enemy.rect.center[1]:
                direction.y = speed
            elif Player.rect.center[1] < enemy.rect.center[1]:
                direction.y = -speed

            enemy.rect.center += direction

    # start battle
    def attackPlayer(self):
        if (self.player_enemy_collision()) and (Player.hit):
            Player.hit = False
            Game.run = "battle"


class Battle():
    # initializing
    def __init__(self):
        super().__init__()
        Battle.sprites = []
        Battle.spritesPath = Game.path("sprites", "battle")
        Battle.screen = "standard"
        Battle.options = 1

        for file in os.listdir(Battle.spritesPath):
            sprite = pygame.image.load(Battle.spritesPath + "//" + file)
            Battle.sprites.append(sprite)

    # physical attack
    def physical():
        pass

    # magical attack
    def magical():
        pass

    # item screen
    def itemScreen():
        pass
        keys = pygame.key.get_pressed()

    # run away
    def runaway():
        pass

    # battle screen
    def battleScreen():
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if Battle.options != 1:
                Battle.options -= 1
        elif keys[pygame.K_s]:
            if Battle.options != 4:
                Battle.options += 1
        elif keys[pygame.K_SPACE] and Game.ticksToIgnoreSPACE == 0:
            Game.ticksToIgnoreSPACE = 5
            if Battle.options == 1:
                Battle.physical()
            elif Battle.options == 2:
                Battle.magical()
            elif Battle.options == 3:
                Game.run = "items"
            elif Battle.options == 4:
                Battle.runaway()
                Game.playerHitTicks = 0
                Game.playerHitSeconds = 0
                Game.run = "game"
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1
        
        if Game.ticksToIgnoreSPACE > 0:
            Game.ticksToIgnoreSPACE -= 1

        if Battle.options == 1:
            Camera.displaySurface.blit(Battle.sprites[2], (0, 0))
        elif Battle.options == 2:
            Camera.displaySurface.blit(Battle.sprites[1], (0, 0))
        elif Battle.options == 3:
            Camera.displaySurface.blit(Battle.sprites[0], (0, 0))
        elif Battle.options == 4:
            Camera.displaySurface.blit(Battle.sprites[3], (0, 0))

        height = 300
        screenSize = Game.screen.get_size()
        if Player.color == "w":
            Camera.displaySurface.blit(pygame.image.load(Player.path + Player.right).convert_alpha(), (300, screenSize[1] - height))
        elif Player.color == "b":
            Camera.displaySurface.blit(pygame.image.load(Player.path + Player.rightB).convert_alpha(), (300, screenSize[1] - height))
        for enemy in Enemy.list:
            Camera.displaySurface.blit(enemy.image, (900, screenSize[1] - height))


# starting the game
if __name__ == "__main__":
    Game()
