import pygame
import os

from player import Player
from camera import Camera
from enemy import Enemy
from game import Game

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