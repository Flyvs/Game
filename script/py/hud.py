import pygame

class HUD(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, pos: tuple, text: str, font: str, fontSize: int, rgb: tuple):
        super().__init__(group)

        font_ = pygame.font.SysFont(font, fontSize)
        HUD.image = font_.render(text, True, rgb)
        HUD.rect = HUD.image.get_rect(center=pos)


    def updateHUD(text: str, font: str, fontSize: int, rgb: tuple, player, game):
        HUD_w = player.rect.center[0] + (game.screen.get_size()[0] // 2) - 125
        HUD_h = player.rect.center[1] - (game.screen.get_size()[1] // 2) + 25
        pos = (HUD_w, HUD_h)

        font_ = pygame.font.SysFont(font, fontSize)
        HUD.image = font_.render(text, True, rgb)
        HUD.rect = HUD.image.get_rect(center=pos)