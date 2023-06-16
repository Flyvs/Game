import pygame
import os
from msgbox import MsgBox

class NPC(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 pos: tuple,
                 npc_path: str,
                 npc_spawn: str,
                 msgbox: MsgBox):
        
        super().__init__(group)

        self.hitted = False
        self.npc_path = npc_path
        self.msgbox = msgbox

        self.image = pygame.image.load(self.npc_path + self.spawn(npc_spawn)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def spawn(self, npc: str):
        for file in os.listdir(self.npc_path):
            casefoldFile = file[:-4].casefold()
            npc = npc.casefold()
            if casefoldFile == npc:
                return file
            
    def hit(self, rect):
        collision_x = rect.rect[0] + 64 >= self.rect[0] and self.rect[0] + 64 >= rect.rect[0]
        collision_y = rect.rect[1] + 64 >= self.rect[1] and self.rect[1] + 64 >= rect.rect[1]

        if collision_x and collision_y:
            self.msgbox.active = True
        else:
            self.msgbox.active = False
            
        return collision_x and collision_y