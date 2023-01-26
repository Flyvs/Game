import pygame
import os

from npc import NPC
from game import Game

class MsgBox(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        for file in os.listdir(Game.msgboxPath):
            MsgBox.image = pygame.image.load(Game.msgboxPath + file).convert_alpha()
            MsgBox.rect = MsgBox.image.get_rect(topleft=pos)

    def init():
        MsgBox((NPC.rect[0] - 224, NPC.rect[1] - 192), Game.camera)