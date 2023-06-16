import pygame
from PIL import Image
import os

class Merge():   
    def surfaces(path: str, fontsize: int, pos: tuple[int, int], *surfaces: pygame.Surface):
        """
        merges multiple surfaces
        the last surface given will be on top
        :param path: the temporary path where the surfaces will be cached
        :param fontsize: the fontsize of the text. Used to determine the line spacing
        :pos: position of the text
        :param *surfaces: all the surfaces to merge
        """        
        if not os.path.exists(path):
            os.makedirs(path)

        for index, surface in enumerate(surfaces):
            surface.convert_alpha()
            pygame.image.save(surface, f"{path}temp{index}.png")

        background = None
        line_spacing = 0
        x, y = pos[0], pos[1]
        
        for index, file in enumerate(os.listdir(path)):
            foreground = Image.open(f"{path}{file}").convert("RGBA")
            if index == 0:
                background = foreground               
            else:
                y = y + line_spacing
                line_spacing = fontsize // 2 + 5
                background.paste(foreground, (x, y), foreground)
            os.remove(f"{path}{file}")

        tempfinal = f"{path}tempfinal.png"
        background.save(tempfinal)
        surface = pygame.image.load(tempfinal)
        os.remove(tempfinal)

        return surface
