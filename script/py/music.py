import pygame
import os
import json

class Music():
    # initializing
    def __init__(self, musicPath: str, game):
        """
        "game" needs to be class type
        """
        super().__init__()

        Music.path = musicPath
        Music.game = game

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

        if Music.game.gamedata["volume"] > 20:
            Music.game.gamedata["volume"] = 20
            volume = Music.game.gamedata["volume"]
        elif Music.game.gamedata["volume"] < 0:
            Music.game.gamedata["volume"] = 0
            volume = Music.game.gamedata["volume"]

        # read json data
        Music.game.gamedatafile = open(Music.game.jsonPath + "gamedata.json", "w")
        json.dump(Music.game.gamedata, Music.game.gamedatafile)
        Music.game.gamedatafile.close()

        self.volume(volume)

    # set volume
    def volume(self, volume: float):
        volume *= 1.5
        volume /= 50
        pygame.mixer.music.set_volume(volume)