import pygame
import os
from pygame_merge import Merge

from PIL import Image, ImageDraw, ImageFont
from typing import Final

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
        RECTANGLE: Final = "rectangle"
        TEXT: Final = "text"

        if not os.path.exists(mergePath):
            os.makedirs(mergePath)

        self.draw(mergePath, width, height, rgbaBox, RECTANGLE)

        image = pygame.image.load(mergePath + "tempRectangle.png")
        os.remove(mergePath + "tempRectangle.png")

        lines = text.split("\n")
        text_surfaces: list[pygame.Surface] = []
        
        if font is None:
            font = "Arial.ttf"
        
        for index, line in enumerate(lines):
            surface_font = ImageFont.truetype(font, fontSize)
            surface_width, surface_height = surface_font.getsize(line)
            name = self.draw(mergePath, surface_width, surface_height, rgbText, TEXT, text, surface_font, index)
            image = pygame.image.load(f"{mergePath}{name}")
            text_surfaces.append(image)

        self.image = Merge.surfaces(mergePath, fontSize, (10, 10), image, *text_surfaces)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, path: str, width: int, height: int, color: tuple, type: str, text: str = None, font: ImageFont.FreeTypeFont = None, index: int = None):
        image = Image.new("RGBA", (width, height), color)
        draw = ImageDraw.Draw(image)

        if type == "rectangle":
            name = f"{path}tempRectangle.png"
            draw.rectangle((0, 0, 0, 0), fill = color)
            image.save(name, format = "PNG")
            return name
        elif type == "text":
            name = f"{path}temp{index}.png"
            draw.text((0, 0), text, font = font, fill = color)
            image.save(name, format = "PNG")
            return name