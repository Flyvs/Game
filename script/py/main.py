import pygame
import os
import json
import sys
from crypting import Crypting
from gamepad import Inputs
from music import Music
from expandList import ExpandList
from camera import Camera

class Game():
    def __init__(self) -> None:
        super().__init__()

        pygame.init()
        pygame.font.init()

        self.export = False

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
        self.pause_sprites = self.path("sprites")

        try:
            os.rename(self.crypting_path + "game_data.rofl", self.crypting_path + "game_data.json")
            os.rename(self.crypting_path + "playerdata.rofl", self.crypting_path + "playerdata.json")

            Crypting.decrypt(self.crypting_path, "game_data.json", "gamekey.key")
            Crypting.decrypt(self.crypting_path, "playerdata.json", "playerkey.key")
        except: pass

        self.game_data_file = open(self.json_path + "game_data.json", "r")
        self.game_data = json.load(self.game_data_file)
        self.game_data_file.close()

        self.playerdata_file = open(self.json_path + "playerdata.json", "r")
        self.playerdata = json.load(self.playerdata_file)
        self.playerdata_file.close()

        self.screen_x = self.game_data["resolutionx"]
        self.screen_y = self.game_data["resulotiony"]
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

        self.player_loaded = False

        self.player_hit_ticks = 0
        self.player_hit_seconds = 0
        self.player_hit_minutes = 0
        self.player_hit_hours = 0

        self.camera = Camera(self.ground_path)
        self.pause = Pause()

        Ememy.list = []
        enemy_A = Enemy()
        enemy_B = Enemy()
        enemy_C = Enemy()
        ExpandList.expand(Enemy.list, enemy_A, enemy_B, enemy_C)

        NPC.list = []
        npc_A = NPC()
        ExpandList.expand(NPC.list, npc_A)

        self.music = Music(self.music_path, self.game_data)
        self.music.play(1, self.game_data["volume"])

    def run(self):
        while True:
            while self.run == "mainmenu":
                self.gamepad_inputs = Inputs.scan()[0]
                self.run_mainmenu()

            while self.run == "game":
                self.gamepad_inputs = Inputs.scan()[0]

                timer = self.track_time(self.player_hit_ticks, self.player_hit_seconds, self.player_hit_minutes, self.player_hit_hours)
                self.player_hit_ticks = timer["ticks"]
                self.player_hit_seconds = timer["seconds"]
                
                if timer["seconds"] % 3 == 0 and Player.hit is False:
                    self.player_hit_ticks = 0
                    self.player_hit_seconds = 0
                    Player.hit = True
                else:
                    Enemy.findPlayer()
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
        Crypting.encrypt(self.crypting_path, "game_data.json", "gamekey.key")
        Crypting.encrypt(self.crypting_path, "playerdata.json", "playerdata.key")
        os.rename(self.crypting_path + "game_data.json", self.crypting_path + "game_data.rofl")
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

        if newPath != None:
            parentDirectory = os.path.join(parentDirectory, newPath)
        if newPath2 != None:
            parentDirectory = os.path.join(parentDirectory, newPath2)

        parentDirectory = parentDirectory + "\\"
        return parentDirectory

if __name__ == "__main__":
    game = Game()
    game.run()