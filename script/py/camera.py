import pygame
import os

from npc import NPC
from attack import Attack

class Camera(pygame.sprite.Group):
    # initializing
    def __init__(self, game, player):
        """
        "game" and "player" needs to be class type
        """
        super().__init__()
        Camera.displaySurface = pygame.display.get_surface()
    	
        Camera.game = game
        Camera.player = player

        # camera offset
        self.offset = pygame.math.Vector2()
        Camera.half_w = Camera.displaySurface.get_size()[0] // 2
        Camera.half_h = Camera.displaySurface.get_size()[1] // 2

        # ground
        Camera.grounds = []
        groundsPath = Camera.game.path("sprites", "grounds")
        for file in os.listdir(groundsPath):
            ground = groundsPath + file
            Camera.grounds.append(ground)

        Camera.ground(Camera.grounds[0])

        # zoom
        Camera.internal_surf_size = (2500, 2500)
        Camera.internal_surf = pygame.Surface(Camera.internal_surf_size, pygame.SRCALPHA)
        Camera.internal_rect = Camera.internal_surf.get_rect(center=(Camera.half_w, Camera.half_h))
        Camera.internal_surface_size_vector = pygame.math.Vector2(Camera.internal_surf_size)
        Camera.internal_offset = pygame.math.Vector2()
        Camera.internal_offset.x = Camera.internal_surf_size[0] // 2 - Camera.half_w
        Camera.internal_offset.y = Camera.internal_surf_size[1] // 2 - Camera.half_h

    # set ground
    def ground(whichGround: str):
        Camera.ground_surf = pygame.image.load(whichGround).convert_alpha()
        Camera.ground_rect = Camera.ground_surf.get_rect(topleft=(0, 0))
        Camera.basic_height = Camera.ground_surf.get_height()
        Camera.basic_width = Camera.ground_surf.get_width()

    # set camera
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - Camera.half_w
        self.offset.y = target.rect.centery - Camera.half_h

    # drawing
    def custom_draw(self, player, enemyList: list):
        self.center_target_camera(player)
        Camera.internal_surf.fill('#71ddee')
        numOfEnemies = len(enemyList)

        # ground
        ground_offset = Camera.ground_rect.topleft - self.offset + Camera.internal_offset
        Camera.internal_surf.blit(Camera.ground_surf, ground_offset)

        i = 0
        # drawing objects
        Camera.spriteList = self.sprites()#sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
        spriteListLen = len(Camera.spriteList)
        while spriteListLen > i:
            spriteListLen = len(Camera.spriteList)
            obj = str(type(Camera.spriteList[i - 1])).partition(".")[2].split("'")[0]
            if Attack.attacking == False and obj == "Attack":
                del Camera.spriteList[i - 1]
            if str(type(Camera.spriteList[1])).partition(".")[2].split("'")[0] == "Attack":
                del Camera.spriteList[1]
            if NPC.hit(Camera.player) == False and obj == "MsgBox":
                del Camera.spriteList[4 + numOfEnemies]
            if str(type(Camera.spriteList[0])).partition(".")[2].split("'")[0] == "MsgBox":
                del Camera.spriteList[0]
            i += 1
        print(Camera.spriteList)

        for sprite in Camera.spriteList:
            offset_pos = sprite.rect.topleft - self.offset + Camera.internal_offset
            Camera.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(Camera.internal_surf, Camera.internal_surface_size_vector)
        scaled_rect = scaled_surf.get_rect(center=(Camera.half_w, Camera.half_h))
        Camera.displaySurface.blit(scaled_surf, scaled_rect)