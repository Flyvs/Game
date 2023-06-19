import pygame
import os
import json
from camera import Camera
from player import Player
from sound import Music
from gamepad import Inputs

class Menu():
    def __init__(self,
                 menu_sprite_path: str,
                 json_path: str,
                 player_path: str,
                 attack_sprite_path: str,
                 game_data,
                 player_data,
                 camera: Camera,
                 game):
        
        super().__init__()

        self.menu_sprite_path = menu_sprite_path
        self.json_path = json_path
        self.player_path = player_path
        self.attack_sprite_path = attack_sprite_path
        self.game_data = game_data
        self.player_data = player_data
        self.camera = camera
        self.game = game

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

        self.player_loaded = False
        self.ticks_to_ignore_space = 5

        self.player = Player(self.camera,
                             (640, 1780),
                             self.json_path,
                             self.player_path,
                             self.game)

    def dump_data(self, data, json_file: str):
        with open(self.json_path + json_file, "w") as file:
            json.dump(data, file)

    def update(self):
        inputs = Inputs.scan()[0]
        keys = pygame.key.get_pressed()
        return inputs, keys

    def create_list(self, list: str, screen: str):
        for file in os.listdir(self.menu_sprite_path + screen):
            list.append(pygame.image.load(f"{self.menu_sprite_path}\\{screen}\\{file}"))

    def save_options(self, new_res_x: int, new_res_y: int, fullscreen: bool):
        self.game_data["resolutionx"] = new_res_x
        self.game_data["resolutiony"] = new_res_y
        self.game_data["fullscreen"] = fullscreen

        self.dump_data(self.game_data, "gamedata.json")
    
    def save_volume(self):
        self.game_data["volume"] = self.options_slider
        volume = self.game_data["volume"]
        self.game.music.volume(volume)

        self.dump_data(self.game_data, "gamedata.json")

    def volume_screen(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]
        display_volume = pygame.font.SysFont("Aerial", 100)
        volume_surface = display_volume.render(str(self.options_slider), False, (0, 0, 0))

        if self.ticks_to_ignore_space > 0:
            self.ticks_to_ignore_space -= 1

        if keys[pygame.K_a] or (inputs is not None and inputs[23] == 1):
            if self.options_slider != 0:
                self.options_slider -= 1
        elif keys[pygame.K_d] or (inputs is not None and inputs[24] == 1):
            if self.options_slider != 20:
                self.options_slider += 1
        elif (keys[pygame.K_SPACE] and self.ticks_to_ignore_space == 0) or (inputs is not None and inputs[10] == 1 and self.ticks_to_ignore_space == 0):
            self.ticks_to_ignore_space = 5
            self.game.run = "options"

        if self.options_slider == 0:
            self.camera.display_surface.blit(self.volume_options[0], (0, 0))
        elif self.options_slider == 1:
            self.camera.display_surface.blit(self.volume_options[1], (0, 0))
        elif self.options_slider == 2:
            self.camera.display_surface.blit(self.volume_options[12], (0, 0))
        elif self.options_slider == 3:
            self.camera.display_surface.blit(self.volume_options[14], (0, 0))
        elif self.options_slider == 4:
            self.camera.display_surface.blit(self.volume_options[15], (0, 0))
        elif self.options_slider == 5:
            self.camera.display_surface.blit(self.volume_options[16], (0, 0))
        elif self.options_slider == 6:
            self.camera.display_surface.blit(self.volume_options[17], (0, 0))
        elif self.options_slider == 7:
            self.camera.display_surface.blit(self.volume_options[18], (0, 0))
        elif self.options_slider == 8:
            self.camera.display_surface.blit(self.volume_options[19], (0, 0))
        elif self.options_slider == 9:
            self.camera.display_surface.blit(self.volume_options[20], (0, 0))
        elif self.options_slider == 10:
            self.camera.display_surface.blit(self.volume_options[2], (0, 0))
        elif self.options_slider == 11:
            self.camera.display_surface.blit(self.volume_options[3], (0, 0))
        elif self.options_slider == 12:
            self.camera.display_surface.blit(self.volume_options[4], (0, 0))
        elif self.options_slider == 13:
            self.camera.display_surface.blit(self.volume_options[5], (0, 0))
        elif self.options_slider == 14:
            self.camera.display_surface.blit(self.volume_options[6], (0, 0))
        elif self.options_slider == 15:
            self.camera.display_surface.blit(self.volume_options[7], (0, 0))
        elif self.options_slider == 16:
            self.camera.display_surface.blit(self.volume_options[8], (0, 0))
        elif self.options_slider == 17:
            self.camera.display_surface.blit(self.volume_options[9], (0, 0))
        elif self.options_slider == 18:
            self.camera.display_surface.blit(self.volume_options[10], (0, 0))
        elif self.options_slider == 19:
            self.camera.display_surface.blit(self.volume_options[11], (0, 0))
        elif self.options_slider == 20:
            self.camera.display_surface.blit(self.volume_options[13], (0, 0))

        self.camera.display_surface.blit(pygame.image.load(self.game.path("sprites") + "sliderBackYES.png"), (0, 0))
        self.camera.display_surface.blit(volume_surface, (600, 265))
        self.save_volume()

    def mainmenu_screen(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]
        self.options_accessed = "mainmenu"

        if self.ticks_to_ignore_space > 0:
            self.ticks_to_ignore_space -= 1

        if keys[pygame.K_w] or (inputs is not None and inputs[21] == 1):
            if self.options_mainmenu != 1:
                self.options_mainmenu -= 1
        elif keys[pygame.K_s] or (inputs is not None and inputs[22] == 1):
            if self.options_mainmenu != 4:
                self.options_mainmenu += 1
        elif (keys[pygame.K_SPACE] and self.ticks_to_ignore_space == 0) or (inputs is not None and inputs[10] == 1 and self.ticks_to_ignore_space == 0):
            self.ticks_to_ignore_space = 5

            if self.options_mainmenu == 1:
                if self.player_loaded is False:
                     self.player_loaded = True
                self.player.rect.center = (640, 1780)
                self.game.run = "game"
            elif self.options_mainmenu == 2:
                self.game.run = "game"
            elif self.options_mainmenu == 3:
                self.game.run = "options"
                pygame.time.wait(100)
            elif self.options_mainmenu == 4:
                self.save_options(self.resx, self.resy, self.game.fullscreen)

        if self.options_mainmenu == 1:
            self.camera.display_surface.blit(self.mainmenu_options[3], (0, 0))
        elif self.options_mainmenu == 2:
            self.camera.display_surface.blit(self.mainmenu_options[1], (0, 0))
        elif self.options_mainmenu == 3:
            self.camera.display_surface.blit(self.mainmenu_options[2], (0, 0))
        elif self.options_mainmenu == 4:
            self.camera.display_surface.blit(self.mainmenu_options[0], (0, 0))

    def pause_screen(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]
        self.options_accessed = "pause"

        if self.ticks_to_ignore_space > 0:
            self.ticks_to_ignore_space -= 1

        if keys[pygame.K_w] or (inputs is not None and inputs[21] == 1):
            if self.options_pause_menu != 1:
                self.options_pause_menu -= 1
        elif keys[pygame.K_s] or (inputs is not None and inputs[22] == 1):
            if self.options_pause_menu != 5:
                self.options_pause_menu += 1
        elif (keys[pygame.K_SPACE] and self.ticks_to_ignore_space == 0) or (inputs is not None and inputs[10] == 1 and self.ticks_to_ignore_space == 0):
            self.ticks_to_ignore_space = 5
            if self.options_pause_menu == 1:
                self.game.run = "options"
            elif self.options_pause_menu == 2:
                self.save_options(self.resx, self.resy, self.game.fullscreen)
            elif self.options_pause_menu == 3:
                self.game.run = "game"
            elif self.options_pause_menu == 4:
                self.save_options(self.resx, self.resy, self.game.fullscreen)
                self.game.run = "mainmenu"
            elif self.options_pause_menu == 5:
                self.save_options(self.resx, self.resy, self.game.fullscreen)
                self.game.exit()

        if self.options_pause_menu == 1:
            self.camera.display_surface.blit(self.pause_options[2], (0, 0))
        elif self.options_pause_menu == 2:
            self.camera.display_surface.blit(self.pause_options[4], (0, 0))
        elif self.options_pause_menu == 3:
            self.camera.display_surface.blit(self.pause_options[3], (0, 0))
        elif self.options_pause_menu == 4:
            self.camera.display_surface.blit(self.pause_options[1], (0, 0))
        elif self.options_pause_menu == 5:
            self.camera.display_surface.blit(self.pause_options[0], (0, 0))

    def options_screen(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]

        if self.ticks_to_ignore_space > 0:
            self.ticks_to_ignore_space -= 1

        if keys[pygame.K_w] or (inputs is not None and inputs[21] == 1):
            if self.options_option_menu != 1:
                self.options_option_menu -= 1
        elif keys[pygame.K_s] or (inputs is not None and inputs[22] == 1):
            if self.options_option_menu != 3:
                self.options_option_menu += 1
        elif (keys[pygame.K_SPACE] and self.ticks_to_ignore_space == 0) or (inputs is not None and inputs[10] == 1 and self.ticks_to_ignore_space == 0):
            self.ticks_to_ignore_space = 5
            if self.options_option_menu == 1:
                self.game.run = "resolution"
                pygame.time.wait(100)
                pass
            elif self.options_option_menu == 2:
                self.game.run = "volume"
                pygame.time.wait(100)
            elif self.options_option_menu == 3:
                if self.options_accessed == "mainmenu":
                    self.game.run = "mainmenu"
                elif self.options_accessed == "pause":
                    self.game.run = "pause"
                pygame.time.wait(100)

        if self.options_option_menu == 1:
            self.camera.display_surface.blit(self.option_options[1], (0, 0))
        elif self.options_option_menu == 2:
            self.camera.display_surface.blit(self.option_options[2], (0, 0))
        elif self.options_option_menu == 3:
            self.camera.display_surface.blit(self.option_options[0], (0, 0))

    def resolution_screen(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]

        if self.ticks_to_ignore_space > 0:
            self.ticks_to_ignore_space -= 1

        if keys[pygame.K_w] or (inputs is not None and inputs[21] == 1):
            if self.options_resolution != 1:
                self.options_resolution -= 1
        elif keys[pygame.K_s] or (inputs is not None and inputs[22] == 1):
            if self.options_resolution != 6:
                self.options_resolution += 1
        elif (keys[pygame.K_SPACE] and self.ticks_to_ignore_space == 0) or (inputs is not None and inputs[10] == 1 and self.ticks_to_ignore_space == 0):
            self.ticks_to_ignore_space = 5
            if self.options_resolution == 1:
                self.resx = 1280
                self.resy = 720
                self.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 2:
                self.resx = 1920
                self.resy = 1080
                self.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 3:
                self.resx = 1920
                self.resy = 1080
                self.game.fullscreen = True
                self.screen = pygame.display.set_mode((self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 4:
                self.resx = 2560
                self.resy = 1080
                self.game.fullscreen = False
                self.screen = pygame.display.set_mode((self.resx, self.resy))
            elif self.options_resolution == 5:
                self.resx = 3440
                self.resy = 1440
                self.game.fullscreen = True
                self.screen = pygame.display.set_mode((self.resx, self.resy), pygame.FULLSCREEN)
            elif self.options_resolution == 6:
                self.game.run = "options"
                self.save_options(self.resx, self.resy, self.game.fullscreen)
                pygame.time.wait(100)

        if self.options_resolution == 1:
            self.camera.display_surface.blit(self.resolution_options[0], (0, 0))
        elif self.options_resolution == 2:
            self.camera.display_surface.blit(self.resolution_options[1], (0, 0))
        elif self.options_resolution == 3:
            self.camera.display_surface.blit(self.resolution_options[2], (0, 0))
        elif self.options_resolution == 4:
            self.camera.display_surface.blit(self.resolution_options[3], (0, 0))
        elif self.options_resolution == 5:
            self.camera.display_surface.blit(self.resolution_options[4], (0, 0))
        elif self.options_resolution == 6:
            self.camera.display_surface.blit(self.resolution_options[5], (0, 0))

        self.camera.half_w = self.camera.display_surface.get_size()[0] // 2
        self.camera.half_h = self.camera.display_surface.get_size()[1] // 2
        self.camera.internal_offset.x = self.camera.internal_surf_size[0] // 2 - self.camera.half_w
        self.camera.internal_offset.y = self.camera.internal_surf_size[1] // 2 - self.camera.half_h
