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
                 font_size: int,
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

        name_rect = self.draw(mergePath, width, height, rgbaBox, RECTANGLE)

        image = pygame.image.load(name_rect)

        lines = text.split("\n")
        text_surfaces: list[pygame.Surface] = []
        
        if font is None:
            font = "arial.ttf"
        
        for index, line in enumerate(lines):
            surface_font = ImageFont.truetype(font, font_size)
            mask = surface_font.getmask(line)
            surface_width, surface_height = mask.size
            name = self.draw(mergePath, surface_width, surface_height, rgbText, TEXT, line, surface_font, index)

            surface_image = pygame.image.load(name)
            text_surfaces.append(surface_image)

        self.image = Merge.surfaces(mergePath, font_size, (10, 10), 10, image, *text_surfaces)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, path: str, width: int, height: int, color: tuple, type: str, text: str = None, font: ImageFont.FreeTypeFont = None, index: int = None):
        if type == "rectangle":
            image = Image.new("RGBA", (width, height), color)
            draw = ImageDraw.Draw(image)
            name = f"{path}tempRectangle.png"
            draw.rectangle((0, 0, 0, 0), fill = color)
            image.save(name, "PNG")
            return name
        elif type == "text":
            image = Image.new("RGBA", (width, height + 10), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            name = f"{path}temp{index}.png"
            draw.text((0, 0), text, font = font, fill = color)
            image.save(name, "PNG")
            return name