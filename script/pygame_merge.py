import pygame
from PIL import Image
import os


class Merge():
    def surfaces(path: str, *surfaces: pygame.Surface):
        """
        merges multiple surfaces
        the last surface given will be on top
        """
        if not os.path.exists(path):
            os.makedirs(path)
        index = 0
        for surface in surfaces:
            surface.convert_alpha()
            pygame.image.save(surface, path + f"temp{index}.png")
            index += 1
        index = 0
        for file in os.listdir(path):
            if index > 0:
                background = foreground
                foreground = Image.open(path + file).convert("RGBA")
                background.paste(foreground, ((background.width - foreground.width) // 2, (background.height - foreground.height) // 2), foreground)
            else:
                foreground = Image.open(path + file).convert("RGBA")
            index += 1
        background.save(path + "tempfinal.png")
        surface = pygame.image.load(path + "tempfinal.png")
        for file in os.listdir(path):
            os.remove(path + file)
        return surface