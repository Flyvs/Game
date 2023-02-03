import pygame
from PIL import Image
import os


class Merge():
    # method to merge two surfaces in pygame
    def surfaces(surface1: pygame.Surface, surface2: pygame.Surface, path: str):
        surface1.convert_alpha()
        surface2.convert_alpha()
        pygame.image.save(surface1, path + "temp1.png")
        pygame.image.save(surface2, path + "temp2.png")
        img1 = Image.open(path + "temp1.png")
        img2 = Image.open(path + "temp2.png")
        img1.paste(img2, (10, 50))
        img1.save(path + "temp1x2.png")
        surface = pygame.image.load(path + "temp1x2.png")
        os.remove(path + "temp1.png")
        os.remove(path + "temp2.png")
        os.remove(path + "temp1x2.png")
        return surface


        