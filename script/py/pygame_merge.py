import pygame
from PIL import Image
import os

class Merge():   
    def surfaces(path: str, font_size: int, pos: tuple[int, int], extra_space: int = 0, *surfaces: pygame.Surface):
        """
        merges multiple surfaces
        the last surface given will be on top
        :param path: the temporary path where the surfaces will be cached
        :param font_size: the font_size of the text. Used to determine the line spacing
        :param pos: position of the text
        :param extra_space: extra space between text and textbox border
        :param *surfaces: all the surfaces to merge. Last one given will be on top
        """        
        if not os.path.exists(path):
            os.makedirs(path)

        for surface in surfaces:
            surface.convert_alpha()

        background = None
        line_spacing = 0
        x, y = pos[0], pos[1]
        
        files = os.listdir(path)
        files.sort()
        tempRectangle = files.pop(-1)
        files.insert(0, tempRectangle)
        for index, file in enumerate(files):
            foreground = Image.open(f"{path}{file}").convert("RGBA")
            if index == 0:
                background = foreground               
            else:
                y = y + line_spacing
                line_spacing = font_size // 2 + extra_space
                background.paste(foreground, (x, y), foreground)
            os.remove(f"{path}{file}")

        tempfinal = f"{path}tempfinal.png"
        background.save(tempfinal)
        surface = pygame.image.load(tempfinal)
        os.remove(tempfinal)

        return surface
