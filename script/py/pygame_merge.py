import pygame
from PIL import Image
import os

class Merge():
    def surfaces(path: str, *surfaces: pygame.Surface):
        """
        merges multiple surfaces
        the last surface given will be on top
        :param path: the temporary path where the surfaces will be cached
        :param *surfaces: all the surfaces to merge
        """
        if not os.path.exists(path):
            os.makedirs(path)

        for index, surface in enumerate(surfaces):
            surface.convert_alpha()
            pygame.image.save(surface, f"{path}temp{index}.png")

        background = None
        for index, file in enumerate(os.listdir(path)):
            foreground = Image.open(f"{path}{file}").convert("RGBA")
            if index == 0:
                background = foreground               
            else:
                background.paste(foreground, ((background.width - foreground.width) // 2, (background.height - foreground.height) // 2), foreground)
            os.remove(f"{path}{file}")

        background.save(f"{path}tempfinal.png")
        surface = pygame.image.load(f"{path}tempfinal.png")
        os.remove(f"{path}tempfinal.png")

        return surface
