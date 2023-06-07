import pygame
from pygame_merge import Merge
from PIL import Image, ImageDraw
import os

class MsgBox(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos: tuple, text: str, font: str, fontSize: int, rgbText: tuple, rgbaBox: tuple, width: int, height: int, mergePath: str, group):
        super().__init__(group)
        
        if not os.path.exists(mergePath):
            os.makedirs(mergePath)

        self.draw(mergePath, width, height, rgbaBox)

        font_ = pygame.font.SysFont(font, fontSize)
        box = pygame.image.load(mergePath + "tempRectangle.png")
        os.remove(mergePath + "tempRectangle.png")
        text_ = font_.render(text, True, rgbText)
        self.image = Merge.surfaces(mergePath, box, text_)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, path: str, width: int, height: int, color: tuple):
        image = Image.new("RGBA", (width, height), color)
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, 0, 0), fill=color)
        image.save(path + "tempRectangle.png", "PNG")
