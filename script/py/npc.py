import pygame
import os

class NPC(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos: tuple, path: str, group):
        super().__init__(group)

        NPC.hitted = False
        self.path = path

        self.allItems = []
        self.image = pygame.image.load(self.path + self.spawn("testNPC")).convert_alpha()
        NPC.rect = self.image.get_rect(topleft=pos)

    # spawn the npc
    def spawn(self, item: str):
        for file in os.listdir(self.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # check if npc is hit
    def hit(rect: pygame.Rect):
        collision_x = rect.rect[0] + 64 >= NPC.rect[0] and NPC.rect[0] + 64 >= rect.rect[0]
        collision_y = rect.rect[1] + 64 >= NPC.rect[1] and NPC.rect[1] + 64 >= rect.rect[1]
        return collision_y and collision_x