import pygame
import os
import json
from camera import Camera
from music import Music

class Pause():
    def __init__(self, pause_path: str, pause_sprite_path: str, player, game_data):
        super().__init__()

        self.pause_path = pause_path
        self.pause_sprite_path = pause_sprite_path
        self.player = player
        self.game_data = game_data

        self.mainmenu_options = []
        self.pause_options = []
        self.option_options = []
        self.resolution_options = []
        self.volume_options = []

        self.create_list(self.mainmenu_options, "mainmenu")
        self.create_list(self.pause_options, "pause")
        self.create_list(self.option_options, "options")
        self.create_list(self.resolution_options, "resolution")
        self.create_list(self.volume_options, "volumeslider")

        self.options_mainmenu = 1
        self.options_pause_menu = 1
        self.options_option_menu = 1
        self.options_resolution = 1
        self.options_slider = self.game_data["volume"]
        self.options_accessed = ""

        self.resx = self.game_data["resolutionx"]
        self.resy = self.game_data["resolutiony"]

    def create_list(self, list: str, screen: str):
        for file in os.listdir(self.pause_sprite_path):
            list.append(pygame.image.load(f"{self.pause_sprite_path}\\{screen}\\{file}"))

    def save_options(self, new_res_x: int, new_res_y: int, fullscreen: bool):
        self.game_data["resolutionx"] = new_res_x
        self.game_data["resolutiony"] = new_res_y
        self.game_data["fullscreen"] = fullscreen

        self.game_datafile = open(self.pause_path + "gamedata.json", "w")
        json.dump(self.game_data, self.game_datafile)
        self.game_datafile.close()
    
    def save_pos(self):
        try:
            self.game_data["playerx"] = self.player.rect.center[0]
            self.game_data["playery"] = self.player.rect.center[1]

            self.game_datafile = open(self.pause_path + "gamedata.json", "w")
            json.dump(self.game_data, self.game_datafile)
            self.game_datafile.close()
        except: pass

    def load_pos(self):
        if Pause.game.playerLoaded == False:
            Pause.game.player = Pause.player((Pause.game.playerdata["playerx"],
                                              Pause.game.playerdata["playery"]),
                                              Pause.game,
                                              Pause.game.jsonPath,
                                              Pause.game.playerPath,
                                              Pause.game.attackSpritePath,
                                              Pause.game.camera)
            Pause.game.playerLoaded = True

        Pause.game.playerdatafile = open(
            Pause.game.jsonPath + "playerdata.json", "w")
        json.dump(Pause.game.playerdata, Pause.game.playerdatafile)
        Pause.game.playerdatafile.close()