import pygame
from pygame_merge import Merge

class MsgBox(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos: tuple, text: str, font: str, fontSize: int, rgb: tuple, msgbox: str, msgboxPath: str, mergePath: str, group):
        super().__init__(group)

        font_ = pygame.font.SysFont(font, fontSize)
        box = pygame.image.load(msgboxPath + msgbox)
        text_ = font_.render(text, True, rgb)
        self.image = Merge.surfaces(mergePath, box, text_)
        self.rect = self.image.get_rect(topleft=pos)