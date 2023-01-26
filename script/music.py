import pygame
import os
import json

from main import Game

class Music():
    # initializing
    def __init__(self):
        super().__init__()

        Music.path = Game.path("music")

    # play
    def play(self, song: int, volume: float):
        pygame.mixer.init()
        self.songs = []

        for file in os.listdir(Music.path):
            self.songs.append(file)

        pygame.mixer.music.load(Music.path + self.songs[song])
        pygame.mixer.music.play(-1, 0, 0)

        # can be deleted if found out how to make the json inaccessable
        if Game.data["volume"] > 20:
            # can be deleted if found out how to make the json inaccessable
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
        volume /= 50
        pygame.mixer.music.set_volume(volume)