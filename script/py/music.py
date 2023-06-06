import pygame
import os
import json

class Music():
    def __init__(self, music_path: str, game_data):
        super().__init__()

        self.music_path = music_path
        self.game_data = game_data

        self.songs = []
        pygame.mixer.init()

        for file in os.listdir(self.music_path):
            self.songs.append(file)

    def play(self, song: int, volume: float):
        song = song - 1

        try:
            pygame.mixer.music.load(self.music_path + self.songs[song])
            pygame.mixer.music.play(-1, 0, 0)
        except: pass

        if self.game_data["volume"] > 20:
            self.game_data["volume"] = 20
            volume = self.game_data["volume"]
        elif self.game_data["volume"] < 0:
            self.game_data["volume"] = 0
            volume = self.game_data["volume"]

        game_data_file = open(self.music_path + "gamedata.json", "w")
        json.dump(self.game_data, game_data_file)
        game_data_file.close()

        self.volume(volume)

    def volume(self, volume: float):
        volume *= 1.5
        volume /= 50
        pygame.mixer.music.set_volume(volume)
