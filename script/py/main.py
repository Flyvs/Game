import pygame
import os
import json
import sys
from typing import List, Final
import cryptography.fernet

from popup import Error
from crypting import Crypting
from gamepad import Inputs
from sound import Music
from expandList import ExpandList
from camera import Camera
from menu import Menu
from enemy import Enemy
from attack import Attack
from npc import NPC
from msgbox import MsgBox

class Game():
    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.font.init()

        self.export = False # set this to true when converting to an .exe

        self.json_path = self.path("script")
        self.msgbox_path = self.path("sprites", "msgboxes")
        self.enemy_path = self.path("sprites", "enemies")
        self.merge_path = self.path("temp")
        self.npc_path = self.path("sprites", "NPCs")
        self.player_path = self.path("sprites", "player")
        self.attacksprite_path = self.path("sprites", "attack")
        self.music_path = self.path("music")
        self.crypting_path = self.json_path
        self.ground_path = self.path("sprites", "grounds")
        self.menu_sprites = self.path("sprites")
        
        FONTSIZE: Final = 20

        try:
            os.rename(self.crypting_path + "gamedata.rofl", self.crypting_path + "gamedata.json")
            os.rename(self.crypting_path + "playerdata.rofl", self.crypting_path + "playerdata.json")
            Crypting.decrypt("gamedata.json", "gamekey.key", self.crypting_path)
            Crypting.decrypt("playerdata.json", "playerkey.key", self.crypting_path)
        except: pass

        with open(self.json_path + "gamedata.json", "r") as self.game_data_file:
            self.game_data = json.load(self.game_data_file)

        with open(self.json_path + "playerdata.json", "r") as self.playerdata_file:
            self.player_data = json.load(self.playerdata_file)

        self.screen_x = self.game_data["resolutionx"]
        self.screen_y = self.game_data["resolutiony"]
        self.fullscreen = self.game_data["fullscreen"]

        if not self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), pygame.FULLSCREEN)

        pygame.display.set_caption("DragonRogue")
        pygame.display.set_icon(pygame.image.load(self.path("sprites", "player") + "playerR.png"))

        self.clock = pygame.time.Clock()
        self.run = "mainmenu"
        self.ground = "ground:0"

        self.ticks_to_ignore_tab = 0
        self.ticks_to_ignore_space = 0

        self.player_hit_ticks = 0
        self.player_hit_seconds = 0
        self.player_hit_minutes = 0
        self.player_hit_hours = 0

        self.camera = Camera(self.ground_path)
        self.menu = Menu(self.menu_sprites,
                         self.json_path,
                         self.player_path,
                         self.attacksprite_path, 
                         self.game_data,
                         self.player_data,
                         self.camera,
                         self)
        self.player = self.menu.player

        self.attack_list: List[Attack] = []
        attack_A = Attack(group = self.camera,
                          TYPE = "classic",
                          DMG = 5,
                          sprite_path = self.path("sprites", "attack"),
                          sprite_left = "attackLeft.png",
                          sprite_right = "attackRight.png",
                          width = 30,
                          height = 24,
                          player = self.player,
                          game = self)
        ExpandList.expand(self.attack_list, attack_A)

        self.enemy_types: List[Enemy] = []
        self.enemy_list: List[Enemy] = []
        enemy_A = Enemy(group = self.camera,
                        POS = (100, 1768),
                        HP = 30, 
                        ATK = 2,
                        DEF = 20,
                        SPEED = 0,
                        SPAWNED = True,
                        SPRITE = "testenemy.png",
                        LIST = self.enemy_list,
                        game = self,
                        player = self.player,
                        type = "A")
        enemy_B = Enemy(group = self.camera,
                    POS = (300, 1768),
                    HP = 15, 
                    ATK = 5,
                    DEF = 15,
                    SPEED = 0,
                    SPAWNED = True,
                    SPRITE = "testenemy2.png",
                    LIST = self.enemy_list,
                    game = self,
                    player = self.player,
                    type = "B")
        enemy_C = Enemy(group = self.camera,
                    POS = (1000, 1768),
                    HP = 5, 
                    ATK = 12,
                    DEF = 5,
                    SPEED = 0,
                    SPAWNED = True,
                    SPRITE = "testenemy3.png",
                    LIST = self.enemy_list,
                    game = self,
                    player = self.player,
                    type = "C")
        ExpandList.expand(self.enemy_types, enemy_A, enemy_B, enemy_C)
        self.spawn_test_enemies()

        msgbox_A = MsgBox(group=self.camera,
                          pos = (500 - 224, 1768 - 192),
                          text = "Idk what I could write here to fill the space so I type some random bullshit",
                          font = None,
                          font_size = FONTSIZE,
                          rgbText = (66, 135, 245),
                          rgbaBox = (255, 200, 0, 255),
                          width = 512,
                          height = 128,
                          mergePath = self.path("temp"))
        msgbox_B = MsgBox(group=self.camera,
                          pos = (1200 - 224, 1768 - 192),
                          text = "This is another demo text\nwith a linebreak\nand another linebreak and this is not a linebreak",
                          font = None,
                          font_size = FONTSIZE,
                          rgbText = (255, 255, 255),
                          rgbaBox = (0, 0, 0, 255),
                          width = 560,
                          height = 128,
                          mergePath = self.path("temp"))

        self.npc_list: List[NPC] = []
        npc_A = NPC(group = self.camera,
                    pos = (500, 1768),
                    npc_path = self.npc_path,
                    npc_spawn = "testNPC",
                    msgbox = msgbox_A)
        npc_B = NPC(group = self.camera,
                    pos = (1200, 1768),
                    npc_path = self.npc_path,
                    npc_spawn = "testNPC",
                    msgbox = msgbox_B)
        ExpandList.expand(self.npc_list, npc_A, npc_B)

        self.player.current_attack = self.attack_list[0]
        self.player.npc_list = self.npc_list
        self.player.attack_list = self.attack_list
        self.attack_list = self.attack_list

        self.camera.npc_list = self.npc_list
        self.camera.attack_list = self.attack_list
        self.camera.current_attack = self.player.current_attack
        
        for enemy in self.enemy_list:
            self.player.enemy_list.append(enemy)
            enemy.attack_list = self.attack_list
            enemy.current_attack = self.player.current_attack

        self.music = Music(self.music_path, self.game_data)
        self.music.play(1, self.game_data["volume"])
        
    def spawn_test_enemies(self): # spawn condition will be changed
        for enemy in self.enemy_types:
            self.enemy_list.append(enemy)

    def start(self):
        while True:
            while self.run == "mainmenu":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_mainmenu()

            while self.run == "game":
                self.gamepad_inputs = Inputs.scan()[0]
                for enemy in self.enemy_list:
                    enemy.find_player()
                self.run_game()
            
            while self.run == "pause":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_pause()

            while self.run == "options":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_options()

            while self.run == "resolution":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_resolution()

            while self.run == "volume":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_volume()

    def exit(self):
        Crypting.encrypt("gamedata.json", "gamekey.key", self.crypting_path)
        Crypting.encrypt("playerdata.json", "playerkey.key", self.crypting_path)
        os.rename(self.crypting_path + "gamedata.json", self.crypting_path + "gamedata.rofl")
        os.rename(self.crypting_path + "playerdata.json", self.crypting_path + "playerdata.rofl")

        pygame.quit()
        sys.exit()

    def get_name(self, file: str):
        chars = []
        for char in file:
            chars.append(char)
        chars.reverse()
        file_chars = []

        for chars in chars:
            if not char == "\\":
                file_chars.append(char)
            else:
                file_chars.reverse()
                break

        file = "".join(file_chars)
        return file

    def path(self, newPath: str = None, newPath2: str = None):
        absolutePath = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
        fileDirectory = os.path.dirname(absolutePath)
        parentDirectory = os.path.dirname(fileDirectory)

        if self.export:
            dirName = os.path.abspath(__file__)
            dirName = os.path.dirname(os.path.dirname(dirName))
            parentDirectory = os.path.join(parentDirectory, self.get_name(dirName))
            parentDirectory = os.path.join(parentDirectory, self.get_name(__file__[:-3]))

        if newPath is not None:
            parentDirectory = os.path.join(parentDirectory, newPath)
        if newPath2 is not None:
            parentDirectory = os.path.join(parentDirectory, newPath2)

        parentDirectory = parentDirectory + "\\"
        return parentDirectory

    def tp(self, current_ground: str, new_ground: str, hitbox_x: int, hitbox_y: int, hitbox_w: int, hitbox_h: int, new_pos: tuple):
        if self.player.player_tp_collision(hitbox_x, hitbox_y, hitbox_w, hitbox_h) and self.ground == current_ground:
            self.camera.ground(self.camera.grounds[1])
            self.player.rect.center = new_pos
            self.ground = new_ground

    def timer(self, ticks: int, seconds: int, minutes: int, hours: int):
        ticks += 1

        if ticks >= 60:
            seconds += 1
            ticks = 0

        if seconds >= 60:
            minutes += 1
            seconds = 0

        if minutes >= 60:
            hours += 1
            minutes = 0

        return {"ticks": ticks, "seconds": seconds, "minutes": minutes, "hours": hours}

    def run_default(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = "pause"
        
        if self.gamepad_inputs is not None and self.gamepad_inputs[6] == 1:
            self.run = "pause"

        self.screen.fill("#71ddee")
        self.camera.update()
        self.camera.custom_draw(self.player, self.enemy_list)
        pygame.display.update()
        self.clock.tick(60)

    def run_pause(self):
        self.run_default()
        
        self.screen.fill("#71ddee")
        self.menu.pause_screen()
        pygame.display.update()
        self.clock.tick(20)

    def run_options(self):
        self.run_default()

        self.screen.fill("#71ddee")
        self.menu.options_screen()
        pygame.display.update()
        self.clock.tick(20)

    def run_resolution(self):
        self.run_default()
        
        self.screen.fill("#71ddee")
        self.menu.resolution_screen()
        pygame.display.update()
        self.clock.tick(20)

    def run_mainmenu(self):
        self.run_default()

        self.screen.fill("#71ddee")
        self.menu.mainmenu_screen()
        pygame.display.update()
        self.clock.tick(20)

    def run_volume(self):
        self.run_default()

        self.screen.fill('#71ddee')
        self.menu.volume_screen()
        pygame.display.update()
        self.clock.tick(20)

if __name__ == "__main__":
    fix = "\nIf one of those are missing, try downloading:\n-gamedata.rofl\n-gamekey.key\n-playerdata.rofl\n-playerkey.key\nfrom https://github.com/Flyvs/Game/tree/master/script \npaste the files to \DragonRogue\main\script\nThese 4 files are interdependent, so download and copy them together."
    try:
        game = Game()
        game.start()
    except FileNotFoundError as e:
        Error(f"{e}{fix}")
    except cryptography.fernet.InvalidToken:
        Error(f"The en-/decryption failed! InvalidToken{fix}")
    except json.decoder.JSONDecodeError as e:
        Error(f"A JSON error occured.\n{e}{fix}")