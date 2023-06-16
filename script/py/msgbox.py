import pygame
import os
from pygame_merge import Merge
from PIL import Image, ImageDraw

class MsgBox(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 pos: tuple,
                 text: str,
                 font: str,
                 fontSize: int,
                 rgbText: tuple,
                 rgbaBox: tuple,
                 width: int,
                 height: int,
                 mergePath: str):
        
        super().__init__(group)

        self.active = False

        if not os.path.exists(mergePath):
            os.makedirs(mergePath)

        self.draw(mergePath, width, height, rgbaBox)

        font_ = pygame.font.SysFont(font, fontSize)
        image = pygame.image.load(mergePath + "tempRectangle.png")
        os.remove(mergePath + "tempRectangle.png")

        lines = text.split("\n")
        text_surfaces = []
        for line in lines:
            text_surfaces.append(font_.render(line, True, rgbText))

        self.image = Merge.surfaces(mergePath, image, *text_surfaces)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, path: str, width: int, height: int, color: tuple):
        image = Image.new("RGBA", (width, height), color)
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, 0, 0), fill=color)
        image.save(path + "tempRectangle.png", "PNG")