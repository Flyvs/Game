import os
import pygame

from camera import Camera
from enemy import Enemy

class Battle():
    # initializing
    def __init__(self, game, player):
        """
        "game" and "player" needs to be class type
        """
        super().__init__()
        Battle.game = game
        Battle.player = player
        Battle.sprites = []
        Battle.spritesPath = Battle.game.path("sprites", "battle")
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

        if keys[pygame.K_w] or (Battle.game.gamepadInputs != None and Battle.game.gamepadInputs[21] == 1):
            if Battle.options != 1:
                Battle.options -= 1
        elif keys[pygame.K_s] or (Battle.game.gamepadInputs != None and Battle.game.gamepadInputs[22] == 1):
            if Battle.options != 4:
                Battle.options += 1
        elif (keys[pygame.K_SPACE] and Battle.game.ticksToIgnoreSPACE == 0) or (Battle.game.gamepadInputs != None and Battle.game.gamepadInputs[10] == 1 and Battle.game.ticksToIgnoreSPACE == 0):
            Battle.game.ticksToIgnoreSPACE = 5
            if Battle.options == 1:
                Battle.physical()
            elif Battle.options == 2:
                Battle.magical()
            elif Battle.options == 3:
                Battle.game.run = "items"
            elif Battle.options == 4:
                Battle.runaway()
                Battle.game.playerHitTicks = 0
                Battle.game.playerHitSeconds = 0
                Battle.game.run = "game"
        
        if Battle.game.ticksToIgnoreSPACE > 0:
            Battle.game.ticksToIgnoreSPACE -= 1
        
        if Battle.game.ticksToIgnoreSPACE > 0:
            Battle.game.ticksToIgnoreSPACE -= 1

        if Battle.options == 1:
            Camera.displaySurface.blit(Battle.sprites[2], (0, 0))
        elif Battle.options == 2:
            Camera.displaySurface.blit(Battle.sprites[1], (0, 0))
        elif Battle.options == 3:
            Camera.displaySurface.blit(Battle.sprites[0], (0, 0))
        elif Battle.options == 4:
            Camera.displaySurface.blit(Battle.sprites[3], (0, 0))

        height = 300
        screenSize = Battle.game.screen.get_size()
        if Battle.player.color == "w":
            Camera.displaySurface.blit(pygame.image.load(Battle.player.path + Battle.player.right).convert_alpha(), (300, screenSize[1] - height))
        elif Battle.player.color == "b":
            Camera.displaySurface.blit(pygame.image.load(Battle.player.path + Battle.player.rightB).convert_alpha(), (300, screenSize[1] - height))
        for enemy in Enemy.list:
            Camera.displaySurface.blit(enemy.image, (900, screenSize[1] - height))