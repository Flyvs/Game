import pygame
from player import Player
from game import Game

class NPC(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        NPC.hitted = False
        NPC.path = Game.path("sprites", "NPCs")

        NPC.allItems = []
        NPC.image = pygame.image.load(NPC.path + NPC.spawn("testNPC")).convert_alpha()
        NPC.rect = NPC.image.get_rect(topleft=pos)

    # spawn the npc
    def spawn(item: str):
        for file in os.listdir(NPC.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # check if npc is hit
    def hit():
        collision_x = Player.rect[0] + 64 >= NPC.rect[0] and NPC.rect[0] + 64 >= Player.rect[0]
        collision_y = Player.rect[1] + 64 >= NPC.rect[1] and NPC.rect[1] + 64 >= Player.rect[1]
        return collision_y and collision_x